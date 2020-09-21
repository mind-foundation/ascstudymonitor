""" Post objects returned from channels """

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any

from ascmonitor.publication import Publication


@dataclass(frozen=True)
class PreparedPost:
    """
    Describes a post created from format.
    The payload can reconstruct a post.
    """

    publication: Publication
    publication_url: str
    payload: Any

    def as_dict(self):
        """ Convert to dict """
        return asdict(self)


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
            publication=post.publication,
            publication_url=post.publication_url,
            payload=post.payload,
            id_=id_,
            created=created,
            response=response,
        )

    def as_dict(self):
        dct = asdict(self)
        dct.update(super().as_dict())
        return dct
