""" Channels format and send documents """

from abc import ABC, abstractmethod


class PostSendException(Exception):
    """ Raised when sending a post fails """


class Post(ABC):
    """
    Abstract base class for a post specific for a channel
    """


class Channel(ABC):
    """ Abstract base class for channels """

    @abstractmethod
    def format(self, document) -> Post:
        """ Format a document to return a post """

    @abstractmethod
    def send(self, post: Post):
        """ Send a post via a channel """
