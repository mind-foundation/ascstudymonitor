"""
Provides interface to a post queue built from the event store
"""

from ascmonitor.events import EventKind


class PostQueue:
    """ Get the next post or view the queue """

    def __init__(self, event_store, channel):
        """ Built a new post queue """
        self.event_store = event_store
        self.channel = channel

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
