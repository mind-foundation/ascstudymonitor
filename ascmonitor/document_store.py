""" Store documents in Mendeley """
from typing import Optional

from ascmonitor import DocumentType
from ascmonitor.config import cache_expires
from ascmonitor.document_cache import DocumentCache
from ascmonitor.events import NewDocEvent, UpdatedDocEvent, DeletedDocEvent
from ascmonitor.mendeleur import Mendeleur


class DocumentStore:
    """ Access to documents """

    def __init__(self, authinfo, mongo, event_store, group_id):
        self._mendeley = Mendeleur(authinfo, group_id)
        self._cache = DocumentCache(mongo, self._mendeley.all_documents, cache_expires)
        self._event_store = event_store

    @property
    def documents(self):
        """ Return documents """
        docs, changes = self._cache.get()
        self._emit_events(changes)
        return docs

    def update(self):
        """ Force update """
        changes = self._cache.update()
        self._emit_events(changes)

    def get_by_id(self, id_: str) -> Optional[DocumentType]:
        """ Return document by slug or None if not found """
        return self._cache.get_by_id(id_)

    def get_by_slug(self, slug: str) -> Optional[DocumentType]:
        """ Return document by slug or None if not found """
        return self._cache.get_by_slug(slug)

    def get_download_url(self, document_id):
        """ Get download link for specified document """
        return self._mendeley.get_download_url(document_id)

    def _emit_events(self, changes):
        """ Put changes in the document store as events """
        event_cls = {"created": NewDocEvent, "removed": DeletedDocEvent, "updated": UpdatedDocEvent}

        events = []
        for kind, docs in changes.items():
            for doc in docs:
                if kind == "created":
                    events.append(event_cls[kind](document=doc, timestamp=doc["created"]))
                else:
                    events.append(event_cls[kind](document=doc))

        self._event_store.put_many(events)
