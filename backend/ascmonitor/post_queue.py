"""
A queue of publications which is specific to a channel.
Documents can be appended, removed or reordered.
The queue can be inspected with a user interface.
"""

from collections.abc import Sequence
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List

from pymongo.database import Database
from pymongo.errors import DuplicateKeyError


lock_timeout = timedelta(seconds=60)


class QueueEmptyException(RuntimeError):
    """ Raised when popping from an empty queue """


class QueueLockedException(RuntimeError):
    """ Raised when operating on a locked queue """


class Queue(Sequence):
    """ Helper class, acts like a list """

    def __init__(self, mongo_doc: Dict[str, Any]):
        """ Parse the mongo document as a queue """
        self._doc = mongo_doc
        self._queue = mongo_doc["queue"]

    def __getitem__(self, i):
        """ Get item from queue """
        return self._queue[i]

    def __len__(self):
        """ Get length of queue """
        return len(self._queue)

    def append(self, item):
        """ Append item """
        self._queue.append(item)

    def remove(self, item):
        """ Remove item """
        self._queue.remove(item)

    def swap(self, i, j):
        """ Swap items at indices i and j """
        self._queue[j], self._queue[i] = self._queue[i], self._queue[j]

    def pop(self):
        """ Return and remove head """
        return self._queue.pop(0)

    def to_mongo(self) -> Dict[str, Any]:
        """ Return queue as mongo document """
        return self._doc

    def to_list(self) -> List[str]:
        """ Return queue as list """
        return self._queue.copy()


class PostQueue:
    """ Manager of the post queues """

    collection_name = "queues"

    def __init__(self, channel_name: str, mongo: Database):
        """ Initialize the post queue for a channel """
        self._collection = mongo[self.collection_name]
        self.channel = channel_name
        self.lock_name = channel_name + "__lock"

    def view(self) -> List[str]:
        """ Return the queue as a list """
        with self._get_queue() as queue:
            return queue.to_list()

    def append(self, id_: str):
        """
        Append a publication to the end of the queue.
        :raises ValueError: if publication is already in queue
        """
        with self._get_queue() as queue:
            if id_ in queue:
                raise ValueError("Publication already in queue")
            queue.append(id_)

    def move_up(self, id_: str):
        """
        Move an element up in the queue.
        If the element is already in front or doesnt exist, do nothing.
        If there are less than two elements, do nothing.
        """
        with self._get_queue() as queue:
            index = queue.index(id_)
            if index is not None and len(queue) >= 2 and index != 0:
                queue.swap(index, index - 1)

    def move_down(self, id_: str):
        """
        Move an element down in the queue.
        If the element is already in the back or doesnt exist, do nothing.
        If there are less than two elements, do nothing.
        """
        with self._get_queue() as queue:
            index = queue.index(id_)
            if index is not None and len(queue) >= 2 and index != len(queue) - 1:
                queue.swap(index, index + 1)

    def remove(self, id_: str):
        """
        Removes an element from the queue.
        If element not in queue, do nothing.
        """
        with self._get_queue() as queue:
            if id_ in queue:
                queue.remove(id_)

    def pop(self) -> str:
        """ Removes and returns the next element from the queue """
        with self._get_queue() as queue:
            if not queue:
                raise QueueEmptyException("Could not pop, queue is empty")
            return queue.pop()

    @contextmanager
    def _get_queue(self):
        """
        Lock and retrieve the queue document.
        Use as contextmanager.
        """
        # lock the queue
        now = datetime.now()
        try:
            self._collection.insert_one({"_id": self.lock_name, "timestamp": now})
        except DuplicateKeyError as exc:
            lock = self._collection.find_one({"_id": self.lock_name})
            if lock["timestamp"] > now + lock_timeout:
                # override the lock
                self._collection.update_one({"_id": self.lock_name}, {"timestamp": now})
            else:
                raise QueueLockedException("Queue is locked") from exc

        try:
            # fetch and yield the queue
            queue_doc = self._collection.find_one({"_id": self.channel})
            if queue_doc is None:
                # queue is empty
                queue_doc = {"_id": self.channel, "queue": []}

            queue = Queue(queue_doc)
            yield queue

            # update the queue
            self._collection.replace_one(
                {"_id": self.channel}, queue.to_mongo(), upsert=True
            )
        finally:
            # release the lock
            self._collection.delete_one({"_id": self.lock_name})
