"""
Stores the document library in a database
"""
from datetime import datetime, timedelta


class DocumentCache:
    """ Provides access to stored document data. """

    collection_name = "documents"
    meta_collection_name = "documents_meta"

    def __init__(self, mongo, source_fn, expires):
        """
        :param mongo: mongo db instance
        :param source_fn: function that is called on cache miss
        :param expires: expiration time of cache in seconds
        """
        self._mongo = mongo
        self._collection = mongo[self.collection_name]
        self._meta = mongo[self.meta_collection_name]
        self._source_fn = source_fn
        self._expires = expires

        # reset cache
        self.expire()

    @property
    def expired(self):
        """ Returns True if cache has expired """
        now = datetime.now()
        meta_doc = self._meta.find_one()
        if meta_doc is None:
            return True
        return meta_doc["expiry"] > now

    def get(self):
        """ Get the documents """
        if not self.expired:
            documents = self._get_from_cache()
        else:
            documents = self._get_from_source()
        return documents

    def expire(self):
        """ Clear cache """
        self._meta.drop()
        self._collection.drop()
        self._collection.create_index("slug")

    def _get_from_cache(self):
        """ Return from cache or None """
        data = list(self._collection.find())
        return data

    @staticmethod
    def _set_id_field(documents, field):
        """ Set custom id from field as mongo id """
        return [{"_id": d[field], **d} for d in documents]

    def _get_from_source(self):
        """ Return from source and put in cache """
        documents = self._source_fn()
        documents = self._set_id_field(documents, "id")
        self.put(documents)
        return documents

    def put(self, documents):
        """ Update documents in collection and set expiration """
        self.expire()
        self._collection.insert_many(documents)
        self._meta.insert({"expiry": datetime.now() + timedelta(seconds=self._expires)})
