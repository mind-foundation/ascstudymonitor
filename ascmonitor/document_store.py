""" Store documents in Mendeley """
from ascmonitor.config import cache_expires
from ascmonitor.document_cache import DocumentCache
from ascmonitor.mendeleur import Mendeleur


class DocumentStore:
    """ Access to documents """

    def __init__(self, authinfo, mongo, group_id):
        self._mendeley = Mendeleur(authinfo, group_id)
        self._cache = DocumentCache(mongo, self._mendeley.all_documents, cache_expires)

    @property
    def documents(self):
        """ Return documents """
        return self._cache.get()

    def update(self):
        """ Force update """
        self._cache.expire()
        self._cache.get()

    def get_download_url(self, document_id):
        """ Get download link for specified document """
        return self._mendeley.get_download_url(document_id)
