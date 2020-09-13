"""
A queue of documents which is specific to a channel.
Documents can be appended, removed or reordered.
The queue can be inspected with a user interface.
"""

from logging import getLogger
from pymongo.database import Database

from ascmonitor.channels import Channel
from ascmonitor.events import EventKind

logger = getLogger(__name__)


class PostQueue:
    """ Manager of the post queues """

    collection_name = "queues"

    def __init__(self, channel: Channel, mongo: Database):
        """ Initialize the post queue for a channel """
        self._queue = mongo[self.collection_name]
        self.channel = channel
        self._queue.up

    def append(self, document_id: str):
        """
        Append a document to the end of the queue.
        :raises ValueError: if document is already in queue
        """
        ...

    def move_up(self, document_id):
        ...

    def move_down(self, document_id):
        ...

    def remove(self, document_id):
        ...

    def __iter__(self):
        """ Iter all documents in the queue """
        events = self.event_store.query()

        excluded = set()
        for event in events:
            kind = event.kind
            document = event.document

            if kind == EventKind.new_document:
                if document["id"] not in excluded:
                    yield document
            elif kind == EventKind.deleted_document:
                excluded.add(document["id"])
            elif kind == EventKind.post_start and event.channel == self.channel:
                excluded.add(document["id"])
            elif kind == EventKind.post_success and event.channel == self.channel:
                excluded.add(document["id"])
            elif kind == EventKind.post_failure and event.channel == self.channel:
                if event.allow_retry and document["id"] not in excluded:
                    yield document
                    excluded.add(document)

    def pop(self):
        """ Return the next document in the queue """
        return next(iter(self))
