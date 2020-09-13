""" Store and access documents in Mendeley """
from base64 import b64encode, b64decode
from logging import getLogger
from typing import Any, Dict, List, Optional, Union

from pymongo import DESCENDING
from pymongo.database import Database
from pymongo.errors import BulkWriteError
from slugify import slugify

from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur
from ascmonitor.types import DocumentType, DocumentsType, FilterList

logger = getLogger(__name__)


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


def set_id_field(document: DocumentType) -> DocumentType:
    """ Set mendeley id from field as mongo id """
    return {**document, "_id": document["id"]}


def assign_slug(document: DocumentType):
    """ Put slug in document """
    first_id, *_ = document["id"].split("-")
    slug = (
        slugify(document["title"], max_length=60, word_boundary=True) + "-" + first_id
    )
    return {**document, "slug": slug}


def assign_cursor(document: DocumentType) -> DocumentType:
    """ Assign the document a unique cursor """
    cursor = "$".join([document["created"].isoformat(), document["id"]])
    return {**document, "cursor": cursor}


class DocumentStore:
    """ Access to documents """

    collection_name = "documents"  # for documents
    slug_collection_name = "slugs"  # one-to-many mapping: slug -> document id

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

    def get_documents(
        self,
        first: Optional[int] = None,
        cursor: Optional[str] = None,
        filters: Optional[FilterList] = None,
    ) -> DocumentsType:
        """
        Return page of documents.
        :param first: Maximum number of documents to return.
                      If None, return all.
        :param cursor: Cursor to page. If None, return from first document.
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
        logger.debug("Get documents with query: %s", query)
        documents = self._collection.find(query, {"_id": False}).sort(
            "cursor", DESCENDING
        )

        if first is not None:
            documents = documents.limit(first)

        documents = list(documents)

        # encode the cursors
        for doc in documents:
            doc["cursor"] = encode_cursor(doc["cursor"])

        return documents

    def get_by_id(self, id_: str) -> Optional[DocumentType]:
        """ Return document by slug or None if not found """
        document = self._collection.find_one({"_id": id_}, {"_id": False})
        document["cursor"] = encode_cursor(document["cursor"])
        return document

    def get_by_slug(self, slug: str) -> Optional[DocumentType]:
        """ Return document by slug or None if not found """
        slug_doc = self._slugs.find_one({"slug": slug})
        if slug_doc is None:
            return None

        return self.get_by_id(slug_doc["document"])

    def update(self):
        """ Update the document store by fetching from mendeley. """
        documents = self._mendeley.all_documents()
        self.put(documents)

    def get_download_url(self, document_id: str) -> str:
        """ Get download link for specified document """
        return self._mendeley.get_download_url(document_id)

    def put(self, documents: DocumentsType):
        """ Put updated list of documents in document store """
        # preprocess documents
        documents = self._prepare_docs_for_insert(documents)

        # replace documents
        self._collection.delete_many({})
        self._collection.insert_many(documents)

        # update slugs
        self._put_slugs(documents)

    @staticmethod
    def _prepare_docs_for_insert(documents: DocumentsType) -> DocumentsType:
        """
        Run a preprocessing pipeline for documents about to be inserted
        """
        prepared = []
        for doc in documents:
            doc = set_id_field(doc)
            doc = assign_slug(doc)
            doc = assign_cursor(doc)
            prepared.append(doc)
        return prepared

    def _put_slugs(self, documents: DocumentsType):
        """ Update the slug collection """
        slugs = [{"slug": d["slug"], "document": d["_id"]} for d in documents]
        try:
            self._slugs.insert_many(slugs, ordered=False)
        except BulkWriteError:
            # ignore duplicated slugs
            pass
