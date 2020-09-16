"""
A queue of publications which is specific to a channel.
Documents can be appended, removed or reordered.
The queue can be inspected with a user interface.
"""

# pylint: skip-file

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

    def append(self, publication: str):
        """
        Append a publication to the end of the queue.
        :raises ValueError: if publication is already in queue
        """
        ...

    def move_up(self, publication_id):
        ...

    def move_down(self, publication_id):
        ...

    def remove(self, publication_id):
        ...

    def __iter__(self):
        """ Iter all publications in the queue """
        events = self.event_store.query()

        excluded = set()
        for event in events:
            kind = event.kind
            publication = event.publication

            if kind == EventKind.new_publication:
                if publication["id"] not in excluded:
                    yield publication
            elif kind == EventKind.deleted_publication:
                excluded.add(publication["id"])
            elif kind == EventKind.post_start and event.channel == self.channel:
                excluded.add(publication["id"])
            elif kind == EventKind.post_success and event.channel == self.channel:
                excluded.add(publication["id"])
            elif kind == EventKind.post_failure and event.channel == self.channel:
                if event.allow_retry and publication["id"] not in excluded:
                    yield publication
                    excluded.add(publication)

    def pop(self):
        """ Return the next publication in the queue """
        return next(iter(self))
