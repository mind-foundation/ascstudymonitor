""" Base class for posting channels """
from abc import ABC, abstractmethod

from ascmonitor.channels.post import PreparedPost, SentPost
from ascmonitor.publication import Publication


class Channel(ABC):
    """ Abstract base class for channels """

    @property
    @abstractmethod
    def name(self) -> str:
        """ Unique name of channel """

    @abstractmethod
    def format(self, publication: Publication, url: str) -> PreparedPost:
        """ Format a publication to return a post """

    @abstractmethod
    def send(self, post: PreparedPost) -> SentPost:
        """ Send a post via a channel and return updated post """
