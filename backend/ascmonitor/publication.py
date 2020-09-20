"""
Publication data and metadata
"""

from base64 import b64encode, b64decode
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, NewType, Optional

from humps import camelize
from slugify import slugify

PublicationID = NewType("PublicationID", str)


@dataclass(frozen=True)
class Author:
    """ Author of a publication """

    first_name: Optional[str]
    last_name: str

    @classmethod
    def from_dict(cls, document: Dict[str, str]) -> "Author":
        """ Construct from dictionary """
        return cls(
            first_name=document.get("first_name", None), last_name=document["last_name"]
        )

    def as_dict(self):
        """ Return as dict """
        return asdict(self)

    @property
    def text(self) -> str:
        """ Return author name as plain string """
        if self.first_name is None:
            return self.last_name
        return self.first_name + " " + self.last_name


@dataclass(frozen=True)
class Publication:
    """ An academic publication """

    # pylint: disable=too-many-instance-attributes

    id_: PublicationID
    title: str
    abstract: str
    created: datetime
    year: Optional[int]
    authors: List[Author]
    journal: Optional[str]
    websites: List[str]
    disciplines: List[str]
    keywords: List[str]
    file_attached: bool

    _cursor: Optional[str] = None

    @classmethod
    def from_dict(
        cls, document: Dict[str, Any], cursor: Optional[str] = None
    ) -> "Publication":
        """ Construct from dictionary """
        return cls(
            id_=document["id"],
            title=document["title"],
            abstract=document["abstract"],
            created=document["created"],
            year=document.get("year", None),
            authors=[Author.from_dict(author) for author in document["authors"]],
            journal=document.get("journal", None),
            websites=document["websites"],
            disciplines=document["disciplines"],
            keywords=document["keywords"],
            file_attached=document["file_attached"],
            _cursor=cursor,
        )

    def as_dict(self) -> Dict[str, Any]:
        """ Return as dict """
        pub = asdict(self)
        pub["id"] = self.id_
        del pub["id_"]
        del pub["_cursor"]
        return pub

    def as_mongo_doc(self) -> Dict[str, Any]:
        """ Return as mongo document with mongo id """
        pub = self.as_dict()
        pub["_id"] = self.id_
        pub["slug"] = self.slug
        pub["cursor"] = self.cursor
        return pub

    def as_gql_response(self) -> Dict[str, Any]:
        """ Return as GraphQL response """
        pub = self.as_dict()
        pub["slug"] = self.slug
        pub["cursor"] = self.encoded_cursor

        # embed filterable fields
        for field in ["year", "journal", "disciplines", "keywords"]:
            if pub[field] is None:
                continue

            if isinstance(pub[field], list):
                pub[field] = [{"value": val} for val in pub[field]]
            else:
                pub[field] = {"value": pub[field]}

        return camelize(pub)

    @property
    def slug(self):
        """ Get slug for publication """
        first_id, *_ = self.id_.split("-")
        return slugify(self.title, max_length=60, word_boundary=True) + "-" + first_id

    @property
    def cursor(self) -> str:
        """ Return the canonical unique cursor """
        if self._cursor is None:
            return self.created.isoformat() + "/" + self.id_
        return self._cursor

    @property
    def encoded_cursor(self) -> str:
        """ Return base64 encoded cursor """
        return b64encode(self.cursor.encode()).decode()

    @staticmethod
    def decode_cursor(cursor: Optional[str]) -> Optional[str]:
        """ Decode the cursor from base64 string """
        if not cursor:
            return None

        return b64decode(cursor).decode()
