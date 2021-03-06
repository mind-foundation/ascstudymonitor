from datetime import datetime, timedelta
import pytest
from unittest.mock import create_autospec
from unittest.mock import patch
import tweepy as realtweepy
from ascmonitor.channels.channel import Channel
from ascmonitor.events import EventKind
from ascmonitor.channels.twitter import TwitterChannel
from ascmonitor.event_store import EventStore
from ascmonitor.poster import Poster
from ascmonitor.publication_store import PublicationStore

publication_url = "https://host.com/slug"
post_payload = "test post bla bla"


@pytest.fixture
def publication(publications):
    return publications[0]

@pytest.fixture
def tweepy():
    return create_autospec(realtweepy)

@pytest.fixture
def twitter(tweepy):
    with patch("ascmonitor.channels.twitter.tweepy", tweepy):

        channel = TwitterChannel("","","","")
        yield channel

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

def test_twitter_channel(twitter,publication):
    post = twitter.format(publication, url="url")
    twitter.send(post)
    # assert

    return


# def test_twitter(poster, publicationchannel, event_store, channel, posts):
#     result = poster.post(publication, publication_url)
#
#     # test events
#     events = list(event_store.query(publication.id_))
#     assert len(events) == 2
#     assert events[1].kind == EventKind.post_start
#     assert events[0].kind == EventKind.post_success
#     assert events[1].timestamp < events[0].timestamp
#
#     # test posts
#     prepared, sent = posts
#     channel.format.assert_called_once_with(publication, publication_url)
#     channel.send.assert_called_once_with(prepared)
#     assert result == sent
