from datetime import datetime
import pytest

from ascmonitor.events import EventKind, NewDocEvent, DeletedDocEvent
from ascmonitor.event_store import EventStore


@pytest.fixture
def event_store(mongo):
    return EventStore(mongo)


def test_put(event_store):
    event_store.put("1", NewDocEvent(timestamp=datetime(2020, 1, 1)))
    assert event_store._collection.find_one() == {
        "_id": "1",
        "events": [
            {
                "class_name": "NewDocEvent",
                "kind": "new_document",
                "timestamp": datetime(2020, 1, 1),
            }
        ],
    }


def test_put__multiple(event_store):
    event_store.put("1", NewDocEvent(timestamp=datetime(2020, 1, 1)))
    event_store.put("1", DeletedDocEvent(timestamp=datetime(2020, 1, 2)))
    assert event_store._collection.find_one() == {
        "_id": "1",
        "events": [
            {
                "class_name": "NewDocEvent",
                "kind": "new_document",
                "timestamp": datetime(2020, 1, 1),
            },
            {
                "class_name": "DeletedDocEvent",
                "kind": "deleted_document",
                "timestamp": datetime(2020, 1, 2),
            },
        ],
    }


def test_query(event_store):
    event_store.put("1", NewDocEvent(timestamp=datetime(2020, 1, 1)))
    event_store.put("1", DeletedDocEvent(timestamp=datetime(2020, 1, 3)))
    event_store.put("2", NewDocEvent(timestamp=datetime(2020, 1, 2)))

    events = event_store.query(["1"])
    assert list(events) == [
        ("1", DeletedDocEvent(timestamp=datetime(2020, 1, 3))),
        ("1", NewDocEvent(timestamp=datetime(2020, 1, 1))),
    ]


def test_query__kinds(event_store):
    event_store.put("1", NewDocEvent(timestamp=datetime(2020, 1, 1)))
    event_store.put("1", DeletedDocEvent(timestamp=datetime(2020, 1, 3)))
    event_store.put("2", NewDocEvent(timestamp=datetime(2020, 1, 2)))

    events = event_store.query(["1", "2"], kinds=[EventKind.new_document])
    assert list(events) == [
        ("2", NewDocEvent(timestamp=datetime(2020, 1, 2))),
        ("1", NewDocEvent(timestamp=datetime(2020, 1, 1))),
    ]
