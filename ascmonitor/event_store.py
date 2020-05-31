"""
Keep track of changes to the document store
and posted publications.
"""

from typing import List
import pymongo
from ascmonitor.events import BaseEvent, EventKind, event_from_dict


class EventStore:
    """ Put and query events to an event log """

    collection_name = "event_store"

    def __init__(self, mongo):
        """ Connect the event store to the database """
        self._collection = mongo[self.collection_name]
        self._collection.create_index("timestamp")

    def put(self, event):
        """ Put an event in the event store """
        # probably not needed
        raise NotImplementedError()

    def put_many(self, events: List[BaseEvent]):
        """ Put many events in the event store """
        if not events:
            return
        events_for_db = [e.as_dict() for e in events]
        self._collection.insert_many(events_for_db)

    def query(self, kinds=None):
        """
        Iterate events filtered by event kinds,
        starting with the newest
        """
        if kinds is not None:
            query = {"kind": {"$in": [EventKind(k) for k in kinds]}}
        else:
            query = {}

        events = self._collection.find(query).sort("timestamp", pymongo.DESCENDING)
        events = (event_from_dict(e) for e in events)
        yield from events
