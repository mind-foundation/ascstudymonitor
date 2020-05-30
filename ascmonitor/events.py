""" Events which are put in the EventStore """

from dataclasses import dataclass
from enum import Enum


class EventKind(Enum):
    """ Kind of an event """

    new_document = "new_document"
    updated_document = "updated_document"
    deleted_document = "deleted_document"
    post_start = "post_start"
    post_success = "post_success"
    post_failure = "post_failure"


@dataclass(frozen=True)
class BaseEvent:
    """ Base class for events """

    timestamp: str
    document_id: str
    event_kind: EventKind
