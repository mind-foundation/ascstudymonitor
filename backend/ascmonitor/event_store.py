"""
Keep log of changes to documents
"""

from typing import Iterable, List, Optional, Tuple
from logging import getLogger
import pymongo
from ascmonitor.events import BaseEvent, EventKind, event_from_dict

logger = getLogger(__name__)


class EventStore:
    """ Put and query events to an event log """

    collection_name = "event_store"

    def __init__(self, mongo):
        """ Connect the event store to the database """
        self._collection = mongo[self.collection_name]

    def put(self, document_id: str, event: BaseEvent):
        """ Put an event in the event store """
        logger.debug("Put in document %s event: %s", document_id, event.as_dict())
        query = {"_id": document_id}
        update = {"$push": {"events": event.as_dict()}}
        self._collection.update_one(query, update, upsert=True)

    def query(
        self, document_ids: List[str], kinds: Optional[List[EventKind]] = None
    ) -> Iterable[Tuple[str, BaseEvent]]:
        """
        Iterate events filtered by event kinds,
        starting with the newest
        """
        aggregation = [
            {"$match": {"_id": {"$in": document_ids}}},
            {"$unwind": "$events"},
            {"$sort": {"events.timestamp": pymongo.DESCENDING}},
        ]

        if kinds:
            kind_values = [kind.value for kind in kinds]
            aggregation.append({"$match": {"events.kind": {"$in": kind_values}}})

        events = self._collection.aggregate(aggregation)

        for event in events:
            yield (
                event["_id"],
                event_from_dict(event["events"]),
            )
