""" Store and access publications in Mendeley """
from dataclasses import fields
from logging import getLogger
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from pymongo import DESCENDING, TEXT
from pymongo.database import Database
from pymongo.errors import BulkWriteError

from ascmonitor.events import NewPubEvent, UpdatedPubEvent, DeletedPubEvent
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur
from ascmonitor.ngram_store import Token
from ascmonitor.publication import Author, Publication, PublicationID
from ascmonitor.types import FilterList

logger = getLogger(__name__)

Changes = Tuple[
    Set[PublicationID], Set[PublicationID], Dict[PublicationID, Dict[str, Any]]
]


class PublicationStore:
    """ Database of publications mirroring Mendeley """

    collection_name = "publications"
    slug_collection_name = "slugs"  # one-to-many mapping: slug -> publication id

    def __init__(
        self,
        mendeleur: Mendeleur,
        mongo: Database,
        event_store: EventStore,
    ):
        self._mendeley = mendeleur

        self._mongo = mongo
        self._collection = mongo[self.collection_name]
        self._slugs = mongo[self.slug_collection_name]
        self._event_store = event_store

        self._slugs.create_index("slug", unique=True)
        self._collection.create_index([("cursor", DESCENDING)])

        # let mongodb use index intersection for filters
        self._collection.create_index("year")
        self._collection.create_index("journal")
        self._collection.create_index("disciplines")
        self._collection.create_index("keywords")
        self._collection.create_index("authors")

        # use mongodb text index for full text search
        self._collection.create_index(
            [
                ("title", TEXT),
                ("authors", TEXT),
                ("abstract", TEXT),
                ("keywords", TEXT),
            ]
        )

    def get_publications(
        self,
        first: Optional[int] = None,
        cursor: Optional[str] = None,
        search: Optional[str] = None,
        filters: Optional[FilterList] = None,
    ) -> List[Publication]:
        """
        Return page of publications.
        :param first: Maximum number of publications to return.
                      If None, return all.
        :param cursor: Cursor to page. If None or empty string, return from first publication.
        """
        if first is not None and first <= 0:
            return []

        aggregation = self._build_search_aggregation(first, cursor, search, filters)

        logger.debug("Get publications from mongodb with aggregation: %s", aggregation)
        publications = self._collection.aggregate(aggregation)
        publications = [
            Publication.from_dict(pub, cursor=pub.get("cursor", None))
            for pub in publications
        ]
        return publications

    def search_publications(
        self,
        first: Optional[int] = None,
        cursor: Optional[str] = None,
        search: Optional[str] = None,
        filters: Optional[FilterList] = None,
    ):
        """ Return page for a full text search """

    def get_publications_count(
        self, search: Optional[str] = None, filters: Optional[FilterList] = None
    ):
        """ Get the total count of publications for a query """
        aggregation = self._build_search_aggregation(search=search, filters=filters)
        aggregation += [{"$count": "count"}]
        return self._collection.aggregate(aggregation)["count"]

    def get_distinct(self, field: str) -> List[Dict[str, Any]]:
        """ Return all distinct values for a field and their publication counts """
        # normalization step in aggregation pipeline for every possible field
        try:
            normalization = {
                "year": "$year",
                "authors": "$authors",
                "journal": {"$toLower": "$journal"},
                "disciplines": "$disciplines",
                "keywords": {"$toLower": "$keywords"},
            }[field]
        except KeyError as exc:
            raise ValueError(f"{field} is not a filterable field") from exc

        aggregation = [
            {"$unwind": f"${field}"},
            {"$project": {field: 1}},
            {
                "$group": {
                    "_id": normalization,
                    "value": {"$first": f"${field}"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": False,
                    "value": True,
                    "publicationCount": "$count",
                }
            },
            {"$sort": {"publicationCount": -1}},
        ]

        return list(self._collection.aggregate(aggregation))

    def get_tokens(self) -> List[Token]:
        """ Returns tokens to feed the ngram store """
        field_names = ["year", "authors", "journal", "disciplines", "keywords"]
        textifications: Dict[str, Callable[[Any], str]] = {
            "authors": lambda author: Author.from_dict(author).text,
            "year": str,
        }

        tokens = []
        for field in field_names:
            values = self.get_distinct(field)
            for value in values:
                text = value["value"]
                if field in textifications:
                    text = textifications[field](text)

                token = Token(text=text, field=field, data=value)
                tokens.append(token)

        return tokens

    def count_publications(self, field: str, value: Any) -> int:
        """ Count publications where a field has a specified value """
        return self._collection.count_documents({field: value})

    def get_by_id(self, id_: PublicationID) -> Optional[Publication]:
        """ Return publication by id or None if not found. """
        publication = self._collection.find_one({"_id": id_})
        if publication is None:
            return None

        return Publication.from_dict(publication)

    def get_by_ids(self, ids: List[PublicationID]) -> List[Publication]:
        """ Return multiple publication by ids """
        aggregation = [
            {"$match": {"_id": {"$in": ids}}},
            {"$addFields": {"__order": {"$indexOfArray": [ids, "$_id"]}}},
            {"$sort": {"__order": 1}},
        ]
        publications = self._collection.aggregate(aggregation)
        publications = [Publication.from_dict(pub) for pub in publications]
        return publications

    def get_by_slug(self, slug: str) -> Optional[Publication]:
        """ Return publication by slug or None if not found """
        slug_doc = self._slugs.find_one({"slug": slug})
        if slug_doc is None:
            return None

        return self.get_by_id(slug_doc["publication"])

    def update(self):
        """
        Update the publication store by fetching from mendeley.
        Fails if another process is currently updating the store.
        """
        publications = self._mendeley.all_documents()
        changes = self.put(publications)
        self.emit_changes(changes)

    def get_download_url(self, slug: str) -> str:
        """ Get download link for specified publication """
        slug_doc = self._slugs.find_one({"slug": slug})
        if slug_doc is None:
            raise ValueError("No publication with this slug")
        id_ = slug_doc["publication"]
        return self._mendeley.get_download_url(id_)

    def put(self, publications: List[Publication]) -> Changes:
        """ Replace publications in the database """
        # find changes
        current_publications = self.get_publications()
        changes = self.compare_publications(publications, current_publications)

        # replace publications
        self._collection.delete_many({})
        self._collection.insert_many(pub.as_mongo_doc() for pub in publications)

        # update slugs
        self._put_slugs(publications)

        return changes

    @staticmethod
    def compare_publications(new: List[Publication], old: List[Publication]) -> Changes:
        """
        Compare new pubs with old pubs and save differences as events
        :returns: Triple of created, removed, updated
        """
        old_pubs = {pub.id_: pub for pub in old}
        new_pubs = {pub.id_: pub for pub in new}

        old_ids = set(old_pubs.keys())
        new_ids = set(new_pubs.keys())
        created = new_ids - old_ids
        removed = old_ids - new_ids

        updated: Dict[PublicationID, Dict[str, Any]] = {}
        for id_ in old_ids & new_ids:
            for field in fields(Publication):
                if field.name.startswith("_"):
                    continue

                old_value = getattr(old_pubs[id_], field.name)
                new_value = getattr(new_pubs[id_], field.name)
                if new_value != old_value:
                    updated.setdefault(id_, {})
                    if hasattr(new_value, "as_dict"):
                        new_value = new_value.as_dict()
                    updated[id_][field.name] = new_value

        return created, removed, updated

    def emit_changes(self, changes: Changes):
        """ Emit changes as events in the event store """
        created, removed, updated = changes

        for pub_id in created:
            self._event_store.put(pub_id, NewPubEvent())

        for pub_id in removed:
            self._event_store.put(pub_id, DeletedPubEvent())

        for pub_id, updates in updated.items():
            event = UpdatedPubEvent(updates=updates)
            self._event_store.put(pub_id, event)

    def _build_search_aggregation(
        self,
        first: Optional[int] = None,
        cursor: Optional[str] = None,
        search: Optional[str] = None,
        filters: Optional[FilterList] = None,
    ) -> List[Dict[str, Any]]:
        """ Build a mongo db query as aggregation for a search query """
        query: Dict[str, Any] = {}
        aggregation: List[Dict[str, Any]] = [{"$match": query}]

        if filters is not None:
            for attr, values in filters.items():
                if values:
                    query[attr] = {"$in": values}

        if not search and cursor:
            query["cursor"] = {"$lt": Publication.decode_cursor(cursor)}

        if search:
            query["$text"] = {"$search": search}

            aggregation += [
                {"$addFields": {"score": {"$meta": "textScore"}}},
                {
                    "$addFields": {
                        "cursor": {
                            "$concat": [
                                {
                                    "$toString": {
                                        "$toInt": {"$multiply": ["$score", 1000000]}
                                    }
                                },
                                "/",
                                "$_id",
                            ]
                        }
                    }
                },
            ]

            if cursor:
                aggregation += [
                    {"$match": {"cursor": {"$lt": Publication.decode_cursor(cursor)}}},
                ]

        aggregation += [
            {"$sort": {"cursor": DESCENDING}},
        ]

        if first is not None and first >= 0:
            aggregation += [{"$limit": first}]

        return aggregation

    def _put_slugs(self, publications: List[Publication]):
        """ Update the slug collection """
        slugs = [{"slug": pub.slug, "publication": pub.id_} for pub in publications]
        try:
            self._slugs.insert_many(slugs, ordered=False)
        except BulkWriteError:
            # ignore duplicated slugs
            pass
