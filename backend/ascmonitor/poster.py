""" Common interface for posting from a queue """
# pylint: skip-file

from typing import Any, Dict

from pymongo.database import Database

from ascmonitor.events import PostStartEvent, PostSuccessEvent, PostFailureEvent
from ascmonitor.post_queue import PostQueue
from ascmonitor.channels import PostSendException, SentPost
from ascmonitor.channels.twitter import TwitterChannel
from ascmonitor.publication import Publication


class Poster:
    """ Posts publications to channels """

    def __init__(self, mongo: Database, event_store, publication_store, auths):
        self.mongo = mongo
        self.event_store = event_store
        self.publication_store = publication_store
        self.auths = auths

        # init channels and queues
        self.channels = {"twitter": TwitterChannel(**auths["twitter"])}

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

    def post(
        self, channel_name: str, publication: Publication, url: str
    ) -> Dict[str, Any]:
        """
        Post the next publication in queue
        :param channel: Name of channel to post to
        :raises: KeyError if channel unknown
        """
        channel = self.channels[channel_name]

        self.emit_start(publication, channel_name)
        try:
            post = channel.format(publication, url)
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
