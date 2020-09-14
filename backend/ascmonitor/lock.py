"""
Implements a lock in the mongodb
"""

from contextlib import contextmanager

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class Locked(RuntimeError):
    """ Raised when allready locked """


@contextmanager
def mongo_lock(name: str, collection: Collection):
    """ Context manager that acquires a lock or raises Locked """
    try:
        collection.insert_one({"_id": name})
    except DuplicateKeyError as exc:
        raise Locked() from exc

    yield
    collection.delete_one({"_id": name})
