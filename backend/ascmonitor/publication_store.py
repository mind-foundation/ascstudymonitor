""" Store and access publications in Mendeley """
from base64 import b64encode, b64decode
from logging import getLogger
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from pymongo import DESCENDING, TEXT
from pymongo.database import Database
from pymongo.errors import BulkWriteError
from slugify import slugify

from ascmonitor.events import NewPubEvent, UpdatedPubEvent, DeletedPubEvent
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur
from ascmonitor.ngram_store import Token
from ascmonitor.types import PublicationType, PublicationsType, FilterList

logger = getLogger(__name__)

Changes = Tuple[Set[str], Set[str], Dict[str, Dict[str, Any]]]


class UpdateLocked(RuntimeError):
    """
    Raised when calling update while another process
    is currently updating the store
    """


def encode_cursor(cursor: Optional[str]) -> str:
    """ Encode the cursor as base64 string """
    if cursor is None:
        return ""

    return b64encode(cursor.encode()).decode()


def decode_cursor(cursor: Optional[str]) -> Optional[str]:
    """ Decode the cursor from base64 string """
    if not cursor:
        return None

    return b64decode(cursor).decode()


def set_id_field(publication: PublicationType) -> PublicationType:
    """ Set mendeley id from field as mongo id """
    return {**publication, "_id": publication["id"]}


def assign_slug(publication: PublicationType):
    """ Put slug in publication """
    first_id, *_ = publication["id"].split("-")
    slug = (
        slugify(publication["title"], max_length=60, word_boundary=True)
        + "-"
        + first_id
    )
    return {**publication, "slug": slug}


def assign_cursor(publication: PublicationType) -> PublicationType:
    """ Assign the publication a unique cursor """
    cursor = "$".join([publication["created"].isoformat(), publication["id"]])
    return {**publication, "cursor": cursor}


class PublicationStore:
    """ Database of publications mirroring Mendeley """

    collection_name = "publications"
    slug_collection_name = "slugs"  # one-to-many mapping: slug -> publication id
    lock_collection_name = "locks"

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
        self._lock = mongo[self.lock_collection_name]

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
    ) -> PublicationsType:
        """
        Return page of publications.
        :param first: Maximum number of publications to return.
                      If None, return all.
        :param cursor: Cursor to page. If None or empty string, return from first publication.
        """
        if first is not None and first <= 0:
            return []

        query = self._build_query(search, filters)

        if cursor is not None and cursor != "":
            query["cursor"] = {"$lt": decode_cursor(cursor)}

        logger.debug("Get publications from mongodb with query: %s", query)
        publications = self._collection.find(query, {"_id": False})
        publications = publications.sort("cursor", DESCENDING)
        if first is not None:
            publications = publications.limit(first)

        publications = list(publications)

        # encode the cursors
        for pub in publications:
            pub["cursor"] = encode_cursor(pub["cursor"])

        return publications

    def get_publications_count(
        self, search: Optional[str] = None, filters: Optional[FilterList] = None
    ):
        """ Get the total count of publications for a query """
        query = self._build_query(search, filters)
        return self._collection.count_documents(query)

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
        fields = ["year", "authors", "journal", "disciplines", "keywords"]
        textifications: Dict[str, Callable[[Any], str]] = {
            "authors": lambda author: " ".join(author.values()),
            "year": str,
        }

        tokens = []
        for field in fields:
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

    def get_by_id(self, id_: str) -> Optional[PublicationType]:
        """ Return publication by slug or None if not found """
        publication = self._collection.find_one({"_id": id_}, {"_id": False})
        publication["cursor"] = encode_cursor(publication["cursor"])
        return publication

    def get_by_slug(self, slug: str) -> Optional[PublicationType]:
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

    def get_download_url(self, publication_id: str) -> str:
        """ Get download link for specified publication """
        return self._mendeley.get_download_url(publication_id)

    def put(self, publications: PublicationsType) -> Changes:
        """ Replace publications in the database """
        # preprocess publications
        publications = self._prepare_for_insert(publications)

        # find changes
        current_publications = list(self._collection.find())
        changes = self.compare_publications(publications, current_publications)

        # replace publications
        self._collection.delete_many({})
        self._collection.insert_many(publications)

        # update slugs
        self._put_slugs(publications)

        return changes

    @staticmethod
    def compare_publications(new: PublicationsType, old: PublicationsType) -> Changes:
        """
        Compare new pubs with old pubs and save differences as events
        :returns: Triple of created, removed, updated
        """
        old_pubs = {d["id"]: d for d in old}
        new_pubs = {d["id"]: d for d in new}

        old_ids = set(old_pubs.keys())
        new_ids = set(new_pubs.keys())
        created = new_ids - old_ids
        removed = old_ids - new_ids

        updated: Dict[str, Dict[str, Any]] = {}
        for id_ in old_ids & new_ids:
            for field_name, new_value in new_pubs[id_].items():
                old_value = old_pubs[id_].get(field_name, None)
                if new_value != old_value:
                    updated.setdefault(id_, {})
                    updated[id_][field_name] = new_value

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

    def _build_query(
        self, search: Optional[str] = None, filters: Optional[FilterList] = None
    ) -> Dict[str, Any]:
        """ Build a mongo db query for a search query """
        query: Dict[str, Any] = {}

        if filters is not None:
            for attr, values in filters.items():
                if values is not None:
                    query[attr] = {"$in": values}

        if search is not None and search != "":
            query["$text"] = {"$search": search}

        return query

    @staticmethod
    def _prepare_for_insert(publications: PublicationsType) -> PublicationsType:
        """
        Run a preprocessing pipeline for publications about to be inserted
        """
        prepared = []
        for doc in publications:
            doc = set_id_field(doc)
            doc = assign_slug(doc)
            doc = assign_cursor(doc)
            prepared.append(doc)
        return prepared

    def _put_slugs(self, publications: PublicationsType):
        """ Update the slug collection """
        slugs = [{"slug": d["slug"], "publication": d["_id"]} for d in publications]
        try:
            self._slugs.insert_many(slugs, ordered=False)
        except BulkWriteError:
            # ignore duplicated slugs
            pass
