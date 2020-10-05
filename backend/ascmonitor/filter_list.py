"""
Specifies filter state
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Tuple, Optional

from ascmonitor.publication import Author


@dataclass(frozen=True)
class FilterList:
    """ Represents filters for publications """

    authors: List[Author] = field(default_factory=list)
    journals: List[str] = field(default_factory=list)
    years: List[int] = field(default_factory=list)
    disciplines: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        """ Returns True if no filters set """
        return not any(
            [self.authors, self.journals, self.years, self.disciplines, self.keywords]
        )

    @classmethod
    def from_dict(cls, dct: Optional[Dict[str, List[Any]]]) -> "FilterList":
        """ Parse from dict with flexible field names """
        kwargs: Dict[str, List[Any]] = {}
        if dct is None:
            return cls()

        for key, value in dct.items():
            if key.startswith("author"):
                kwargs["authors"] = [Author.from_dict(author) for author in value]
            elif key.startswith("journal"):
                kwargs["journals"] = value
            elif key.startswith("year"):
                kwargs["years"] = [int(year) for year in value]
            elif key.startswith("discipline"):
                kwargs["disciplines"] = value
            elif key.startswith("keyword"):
                kwargs["keywords"] = value
        return cls(**kwargs)

    def items(self, as_dict=True) -> Iterable[Tuple[str, List[Any]]]:
        """
        Return field -> values mapping, where
        fields are exactly as in database
        """
        if self.authors:
            if as_dict:
                yield "authors", list(author.as_dict() for author in self.authors)
            else:
                yield "authors", self.authors
        if self.years:
            yield "year", self.years
        if self.journals:
            yield "journal", self.journals
        if self.disciplines:
            yield "disciplines", self.disciplines
        if self.keywords:
            yield "keywords", self.keywords

    def iter_flat(self, as_dict=True) -> Iterable[Tuple[str, Any]]:
        """ Iter filters in flat (field, value) form """
        for key, values in self.items(as_dict):
            for value in values:
                yield key, value
