"""
Events which are put in the EventStore.
An event is always associated with a publication.
The event store organized events by publications.
"""
# pylint: disable=too-few-public-methods

from datetime import datetime
from enum import Enum
from typing import Any, Dict
import attr


class EventKind(Enum):
    """ Kind of an event """

    new_publication = "new_publication"
    updated_publication = "updated_publication"
    deleted_publication = "deleted_publication"
    post_start = "post_start"
    post_success = "post_success"
    post_failure = "post_failure"


def event_from_dict(event: Dict[str, Any]) -> "BaseEvent":
    """ Convert event dict to event """
    cls = globals()[event["class_name"]]
    del event["class_name"]
    kind = EventKind(event["kind"])
    assert isinstance(cls, type(BaseEvent))
    return cls(**{**event, "kind": kind})  # type: ignore


@attr.s(frozen=True, auto_attribs=True)
class BaseEvent:
    """
    Base class for events.
    timestamps are in utc
    """

    kind: EventKind
    timestamp: datetime = attr.Factory(datetime.utcnow)

    def as_dict(self):
        """ Return as dict """
        dct = attr.asdict(self)
        dct["kind"] = self.kind.value
        dct["class_name"] = self.__class__.__name__
        return dct


@attr.s(frozen=True, auto_attribs=True)
class NewPubEvent(BaseEvent):
    """ Event """

    kind: EventKind = EventKind.new_publication


@attr.s(frozen=True, auto_attribs=True)
class UpdatedPubEvent(BaseEvent):
    """ Event """

    updates: Dict[str, Any]
    kind: EventKind = EventKind.updated_publication
    timestamp: datetime = attr.Factory(datetime.utcnow)


@attr.s(frozen=True, auto_attribs=True)
class DeletedPubEvent(BaseEvent):
    """ Event """

    kind: EventKind = EventKind.deleted_publication


@attr.s(frozen=True, auto_attribs=True)
class PostStartEvent(BaseEvent):
    """ Event """

    channel: str
    kind: EventKind = EventKind.post_start
    timestamp: datetime = attr.Factory(datetime.utcnow)


@attr.s(frozen=True, auto_attribs=True)
class PostSuccessEvent(BaseEvent):
    """ Event """

    channel: str
    post: Dict[str, Any]
    kind: EventKind = EventKind.post_success
    timestamp: datetime = attr.Factory(datetime.utcnow)


@attr.s(frozen=True, auto_attribs=True)
class PostFailureEvent(BaseEvent):
    """ Event """

    channel: str
    error: str
    allow_retry: bool
    kind: EventKind = EventKind.post_failure
    timestamp: datetime = attr.Factory(datetime.utcnow)
