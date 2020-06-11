""" Common interface for posting from a queue """
from typing import Any, Dict

from ascmonitor import DocumentType
from ascmonitor.events import PostStartEvent, PostSuccessEvent, PostFailureEvent
from ascmonitor.post_queue import PostQueue
from ascmonitor.channels import PostSendException, SentPost
from ascmonitor.channels.twitter import TwitterChannel


class Poster:
    """ Posts documents to channels """

    def __init__(self, event_store, document_store, auths):
        self.event_store = event_store
        self.document_store = document_store
        self.auths = auths

        # init channels and queues
        self.channels = {
            "twitter": {
                "channel": TwitterChannel(**auths["twitter"]),
                "queue": PostQueue(event_store, "twitter"),
            }
        }

    def emit_start(self, document: DocumentType, channel: str):
        """ Notify event store about starting to post """
        event = PostStartEvent(document=document, channel=channel)
        self.event_store.put(event)

    def emit_success(self, document: DocumentType, post: SentPost, channel: str):
        """ Notify event store about a successful post """
        event = PostSuccessEvent(
            document=document, channel=channel, post=post.as_dict(), timestamp=post.created
        )
        self.event_store.put(event)

    def emit_fail(self, document: DocumentType, error: PostSendException, channel: str):
        """ Notify event store about a failed post """
        event = PostFailureEvent(
            document=document, error=error.message, allow_retry=error.allow_retry, channel=channel
        )
        self.event_store.put(event)

    def get_queue(self, channel_name) -> PostQueue:
        """
        Get queue for a channel.
        :raises: KeyError if channel unknown
        """
        return self.channels[channel_name]["queue"]

    def post(self, channel_name) -> Dict[str, Any]:
        """
        Post the next document in queue
        :param channel: Name of channel to post to
        :raises: KeyError if channel unknown
        """
        document_short = self.channels[channel_name]["queue"].pop()
        document = self.document_store.get_by_id(document_short["id"])
        channel = self.channels[channel_name]["channel"]

        self.emit_start(document, channel_name)
        try:
            post = channel.format(document)
            post = channel.send(post)
            self.emit_success(document, post, channel_name)
            return post.as_dict()
        except PostSendException as error:
            self.emit_fail(document, error, channel_name)
            return {"document": document, "channel": channel_name, "error": error.as_dict()}
