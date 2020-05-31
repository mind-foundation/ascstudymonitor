""" Channels format and send documents """

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Optional

from ascmonitor import DocumentType


class PostSendException(Exception):
    """ Raised when sending a post fails """

    def __init__(self, message: str, allow_retry: bool):
        """
        :param message: A human readable error message
        :param allow_retry: True if post should be attempted again
        """
        super().__init__(message)
        self.message = message
        self.allow_retry = allow_retry


@dataclass(frozen=True)
class PreparedPost:
    """
    Describes a post created from format.
    The payload can reconstruct a post.
    """

    document: DocumentType
    channel: "Channel"
    payload: Any

    def as_dict(self):
        dct = asdict(self)
        dct["channel"] = self.channel.name
        return dct


@dataclass(frozen=True)
class SentPost(PreparedPost):
    """
    Describes a sent post with additional infos.
    The response are additional channel specific infos
    """

    id_: str
    created: datetime
    response: Any

    @classmethod
    def from_prepared(
        cls, post: PreparedPost, id_: str, created: datetime, response: Any
    ) -> "SentPost":
        """ Upgrade a PreparedPost """
        return cls(
            document=post.document,
            channel=post.channel,
            payload=post.payload,
            id_=id_,
            created=created,
            response=response,
        )

    def as_dict(self):
        dct = asdict(self)
        dct.update(super().as_dict())
        return dct


class Channel(ABC):
    """ Abstract base class for channels """

    @abstractmethod
    def format(self, document: DocumentType) -> PreparedPost:
        """ Format a document to return a post """

    @abstractmethod
    def send(self, post: PreparedPost) -> SentPost:
        """ Send a post via a channel and return updated post """
