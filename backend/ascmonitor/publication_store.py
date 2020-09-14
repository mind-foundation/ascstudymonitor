""" Store and access publications in Mendeley """
from base64 import b64encode, b64decode
from logging import getLogger
from typing import Any, Dict, Optional, Set, Tuple

from pymongo import DESCENDING
from pymongo.database import Database
from pymongo.errors import BulkWriteError
from slugify import slugify

from ascmonitor.events import NewPubEvent, UpdatedPubEvent, DeletedPubEvent
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur
from ascmonitor.lock import mongo_lock, Locked
from ascmonitor.search_engine import SearchEngine
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

        # create the search engine
        self.search_engine = SearchEngine(self.get_publications())

    def get_publications(
        self,
        first: Optional[int] = None,
        cursor: Optional[str] = None,
        filters: Optional[FilterList] = None,
    ) -> PublicationsType:
        """
        Return page of publications.
        :param first: Maximum number of publications to return.
                      If None, return all.
        :param cursor: Cursor to page. If None, return from first publication.
        """
        query: Dict[str, Any] = {}

        # parse cursor into mongo query
        if cursor:
            query["cursor"] = {"$lt": decode_cursor(cursor)}

        # put filters into mongo query
        if filters is not None:
            for attr, values in filters.items():
                if values is not None:
                    query[attr] = {"$in": values}

        # execute mongodb query
        logger.debug("Get publications with query: %s", query)
        publications = self._collection.find(query, {"_id": False}).sort(
            "cursor", DESCENDING
        )

        if first is not None:
            publications = publications.limit(first)

        publications = list(publications)

        # encode the cursors
        for pub in publications:
            pub["cursor"] = encode_cursor(pub["cursor"])

        return publications

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
        try:
            with mongo_lock("updateLock", self._lock):
                publications = self._mendeley.all_publications()
                changes = self.put(publications)
                self.emit_changes(changes)
                self.search_engine.build_index(publications)
        except Locked as exc:
            raise UpdateLocked("Currently updating in another process") from exc

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
