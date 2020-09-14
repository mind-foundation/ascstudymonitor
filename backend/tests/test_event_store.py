from datetime import datetime
import pytest

from ascmonitor.events import EventKind, NewPubEvent, DeletedPubEvent
from ascmonitor.event_store import EventStore


@pytest.fixture
def event_store(mongo):
    return EventStore(mongo)


def test_put(event_store):
    event_store.put("1", NewPubEvent(timestamp=datetime(2020, 1, 1)))
    assert event_store._collection.find_one() == {
        "_id": "1",
        "events": [
            {
                "class_name": "NewPubEvent",
                "kind": "new_publication",
                "timestamp": datetime(2020, 1, 1),
            }
        ],
    }


def test_put__multiple(event_store):
    event_store.put("1", NewPubEvent(timestamp=datetime(2020, 1, 1)))
    event_store.put("1", DeletedPubEvent(timestamp=datetime(2020, 1, 2)))
    assert event_store._collection.find_one() == {
        "_id": "1",
        "events": [
            {
                "class_name": "NewPubEvent",
                "kind": "new_publication",
                "timestamp": datetime(2020, 1, 1),
            },
            {
                "class_name": "DeletedPubEvent",
                "kind": "deleted_publication",
                "timestamp": datetime(2020, 1, 2),
            },
        ],
    }


def test_query(event_store):
    event_store.put("1", NewPubEvent(timestamp=datetime(2020, 1, 1)))
    event_store.put("1", DeletedPubEvent(timestamp=datetime(2020, 1, 3)))
    event_store.put("2", NewPubEvent(timestamp=datetime(2020, 1, 2)))

    events = event_store.query(["1"])
    assert list(events) == [
        ("1", DeletedPubEvent(timestamp=datetime(2020, 1, 3))),
        ("1", NewPubEvent(timestamp=datetime(2020, 1, 1))),
    ]


def test_query__kinds(event_store):
    event_store.put("1", NewPubEvent(timestamp=datetime(2020, 1, 1)))
    event_store.put("1", DeletedPubEvent(timestamp=datetime(2020, 1, 3)))
    event_store.put("2", NewPubEvent(timestamp=datetime(2020, 1, 2)))

    events = event_store.query(["1", "2"], kinds=[EventKind.new_publication])
    assert list(events) == [
        ("2", NewPubEvent(timestamp=datetime(2020, 1, 2))),
        ("1", NewPubEvent(timestamp=datetime(2020, 1, 1))),
    ]
