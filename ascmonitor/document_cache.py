"""
Stores the document library in a database
"""
import msgpack
from time import sleep


class DocumentCache:
    """ Provides access to stored document data. """

    def __init__(self, redis, source_fn, expires):
        """
        :param redis: redis client instance
        :param source_fn: function that is called on cache miss
        :param expires: expiration time of cache in seconds
        """
        self._redis = redis
        self._source_fn = source_fn
        self._expires = expires

        # reset cache
        self.expire()

    def get(self):
        """ Get the documents """
        documents = self._get_from_cache()
        # sleep(120)
        if documents is None:
            documents = self._get_from_source()
        return documents

    def expire(self):
        """ Clear cache """
        self._redis.delete("documents")

    def _get_from_cache(self):
        """ Return from cache or None """
        data = self._redis.get("documents")
        if data is not None:
            data = msgpack.unpackb(data, raw=False)
        return data

    def _get_from_source(self):
        """ Return from source and put in cache """
        documents = self._source_fn()
        self.put(documents)
        return documents

    def put(self, documents):
        """ Serialize documents, set in redis and set expiration """
        packed = msgpack.packb(documents, use_bin_type=True)
        self._redis.set("documents", packed, ex=self._expires)
