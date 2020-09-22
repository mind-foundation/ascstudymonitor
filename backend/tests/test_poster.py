from datetime import datetime, timedelta
import pytest
from unittest.mock import create_autospec

from ascmonitor.channels.post import PreparedPost, SentPost
from ascmonitor.channels.channel import Channel
from ascmonitor.events import EventKind
from ascmonitor.event_store import EventStore
from ascmonitor.poster import Poster
from ascmonitor.publication_store import PublicationStore

publication_url = "https://host.com/slug"
post_payload = "test post bla bla"


@pytest.fixture
def publication(publications):
    return publications[0]


@pytest.fixture
def posts():
    prepared = PreparedPost(
        publication=publication, publication_url=publication_url, payload=post_payload
    )
    sent = SentPost.from_prepared(
        prepared,
        id_="postid-42",
        created=datetime.now() + timedelta(seconds=120),
        response={"info": [1, 2, 3]},
    )
    return prepared, sent


@pytest.fixture
def channel(publication, posts):
    prepared, sent = posts

    channel = create_autospec(Channel)
    channel.name = "test_channel"
    channel.format.return_value = prepared
    channel.send.return_value = sent
    return channel


@pytest.fixture
def event_store(mongo):
    return EventStore(mongo)


@pytest.fixture
def publication_store():
    return create_autospec(PublicationStore)


@pytest.fixture
def poster(channel, mongo, event_store, publication_store):
    return Poster(
        channel=channel,
        mongo=mongo,
        event_store=event_store,
        publication_store=publication_store,
    )


def test_post(poster, publication, event_store, channel, posts):
    result = poster.post(publication, publication_url)

    # test events
    events = list(event_store.query(publication.id_))
    assert len(events) == 2
    assert events[1].kind == EventKind.post_start
    assert events[0].kind == EventKind.post_success
    assert events[1].timestamp < events[0].timestamp

    # test posts
    prepared, sent = posts
    channel.format.assert_called_once_with(publication, publication_url)
    channel.send.assert_called_once_with(prepared)
    assert result == sent
