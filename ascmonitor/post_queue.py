"""
Provides interface to a post queue built from the event store
"""

from ascmonitor.events import EventKind


class PostQueue:
    """ Get the next post or view the queue """

    def __init__(self, event_store):
        """ Built a new post queue """
        self.event_store = event_store

    def __iter__(self):
        """ Iter all documents in the queue """
        events = self.event_store.query()

        excluded = set()
        yielded = set()
        for event in events:
            document = event.document
            if event.kind == EventKind.new_document:
                if document["id"] not in excluded | yielded:
                    yield document
            elif event.kind == EventKind.deleted_document:
                excluded.add(document["id"])
            elif event.kind == EventKind.post_start:
                excluded.add(document["id"])
            elif event.kind == EventKind.post_success:
                excluded.add(document["id"])
            elif event.kind == EventKind.post_failure:
                if event.allow_retry and event.document["id"] not in excluded | yielded:
                    yield document
                    yielded.add(document)

    def pop(self):
        """ Return the next document in the queue """
        return next(iter(self))
