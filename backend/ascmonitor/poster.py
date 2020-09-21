""" Common interface for posting from a queue """
# pylint: skip-file

from typing import Any, Dict

from pymongo.database import Database

from ascmonitor.channels import Channel
from ascmonitor.event_store import EventStore
from ascmonitor.events import PostStartEvent, PostSuccessEvent, PostFailureEvent
from ascmonitor.post_queue import PostQueue
from ascmonitor.channels import PostSendException, SentPost
from ascmonitor.channels.twitter import TwitterChannel
from ascmonitor.publication import Publication
from ascmonitor.publication_store import PublicationStore


class Poster:
    """ Posts publications to channels """

    def __init__(
        self,
        channel: Channel,
        mongo: Database,
        event_store: EventStore,
        publication_store: PublicationStore,
    ):
        self.event_store = event_store
        self.publication_store = publication_store
        self.channel = channel
        self.post_queue = PostQueue(channel.name, mongo)

    def emit_start(self, publication: Publication, channel: str):
        """ Notify event store about starting to post """
        event = PostStartEvent(channel=channel)
        self.event_store.put(publication.id_, event)

    def emit_success(self, publication: Publication, post: SentPost, channel: str):
        """ Notify event store about a successful post """
        event = PostSuccessEvent(
            channel=channel,
            post=post.as_dict(),
            timestamp=post.created,
        )
        self.event_store.put(publication.id_, event)

    def emit_fail(
        self, publication: Publication, error: PostSendException, channel: str
    ):
        """ Notify event store about a failed post """
        event = PostFailureEvent(
            error=error.message,
            allow_retry=error.allow_retry,
            channel=channel,
        )
        self.event_store.put(publication.id_, event)

    def post(self, publication: Publication, url: str) -> SentPost:
        """ Post a publication """

        self.emit_start(publication, self.channel.name)
        try:
            post = self.channel.format(publication, url)
            post = self.channel.send(post)
            self.emit_success(publication, post, self.channel.name)
            return post
        except PostSendException as error:
            self.emit_fail(publication, error, self.channel.name)
            raise error
