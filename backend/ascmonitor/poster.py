""" Common interface for posting from a queue """
# pylint: skip-file

from typing import Any, Dict

from pymongo.database import Database

from ascmonitor.events import PostStartEvent, PostSuccessEvent, PostFailureEvent
from ascmonitor.post_queue import PostQueue
from ascmonitor.channels import PostSendException, SentPost
from ascmonitor.channels.twitter import TwitterChannel
from ascmonitor.types import PublicationType


class Poster:
    """ Posts publications to channels """

    def __init__(self, mongo: Database, event_store, publication_store, auths):
        self.event_store = event_store
        self.publication_store = publication_store
        self.auths = auths

        # init channels and queues
        self.channels = {"twitter": TwitterChannel(**auths["twitter"])}
        self.queues = {
            "twitter": PostQueue(channel=self.channels["twitter"], mongo=mongo)
        }

    def emit_start(self, publication: PublicationType, channel: str):
        """ Notify event store about starting to post """
        event = PostStartEvent(channel=channel)
        self.event_store.put(publication["id"], event)

    def emit_success(self, publication: PublicationType, post: SentPost, channel: str):
        """ Notify event store about a successful post """
        event = PostSuccessEvent(
            channel=channel,
            post=post.as_dict(),
            timestamp=post.created,
        )
        self.event_store.put(publication["id"], event)

    def emit_fail(
        self, publication: PublicationType, error: PostSendException, channel: str
    ):
        """ Notify event store about a failed post """
        event = PostFailureEvent(
            error=error.message,
            allow_retry=error.allow_retry,
            channel=channel,
        )
        self.event_store.put(publication["id"], event)

    def get_queue(self, channel_name) -> PostQueue:
        """
        Get queue for a channel.
        :raises: KeyError if channel unknown
        """
        return self.channels[channel_name]["queue"]

    def post(self, channel_name) -> Dict[str, Any]:
        """
        Post the next publication in queue
        :param channel: Name of channel to post to
        :raises: KeyError if channel unknown
        """
        # TODO: update publication store before posting

        publication_short = self.channels[channel_name]["queue"].pop()
        publication = self.publication_store.get_by_id(publication_short["id"])
        channel = self.channels[channel_name]["channel"]

        self.emit_start(publication, channel_name)
        try:
            post = channel.format(publication)
            post = channel.send(post)
            self.emit_success(publication, post, channel_name)
            return post.as_dict()
        except PostSendException as error:
            self.emit_fail(publication, error, channel_name)
            return {
                "publication": publication,
                "channel": channel_name,
                "error": error.as_dict(),
            }
