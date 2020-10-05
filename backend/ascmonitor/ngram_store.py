"""
A mongodb powered fuzzy string search engine.
Strings are compared by comparing their n-gram sets.
"""

from dataclasses import dataclass
from itertools import chain
import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

from nltk import everygrams
from pymongo import ASCENDING
from pymongo.database import Database

from ascmonitor.filter_list import FilterList
from ascmonitor.publication_store import PublicationStore

token_regex = re.compile(r"[\W_]+")
min_n = 3
max_n = 3


def get_ngrams(text) -> List[str]:
    """ Get the n-gram decomposition for this token """
    texts = text.strip().lower().split()
    texts = [token_regex.sub("", s) for s in texts]
    ngrams = []
    for subtext in texts:
        ngrams += ["".join(ngram) for ngram in everygrams(subtext, min_n, max_n)]
    return ngrams


@dataclass(frozen=True)
class Token:
    """
    A token which might be associated with a field.
    Text must be a string, but allows storing additional data.
    """

    text: str
    field: str
    data: Optional[Dict[str, Any]]

    @classmethod
    def from_field_value(cls, field: str, value: Any) -> "Token":
        """ Convert a publication field value to a token """
        if hasattr(value, "text"):
            text = value.text.lower()
        else:
            text = str(value).lower()

        if hasattr(value, "as_dict"):
            data = value.as_dict()
        else:
            data = value

        return cls(text=text, field=field, data={"value": data})

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> "Token":
        """ Parse dict """
        return cls(**dct)

    @property
    def ngrams(self) -> List[str]:
        """ N-grams for this token """
        return get_ngrams(self.text)

    def as_entry(self) -> Dict[str, Any]:
        """ Return MongoDB entry for this token """
        return {
            "text": self.text,
            "field": self.field,
            "data": self.data,
            "ngrams": self.ngrams,
        }

    def as_field_text(self) -> Dict[str, Any]:
        """ Return only field and text """
        return {"field": self.field, "text": self.text}

    def __hash__(self):
        return hash((self.text, self.field))


@dataclass(frozen=True)
class TokenResult:
    """ A search result with a token and score """

    text: str
    field: str
    data: Optional[Dict[str, Any]]
    score: float

    @classmethod
    def from_entry(cls, entry: Dict[str, Any]) -> "TokenResult":
        """ Parse a MongoDB entry """
        return cls(
            text=entry["text"],
            field=entry["field"],
            data=entry["data"],
            score=entry["score"],
        )

    def __hash__(self):
        return hash((self.text, self.field, self.score))


class NGramStore:
    """ Fuzzy string search engine """

    collection_name = "ngram_index"

    def __init__(self, mongo: Database):
        self._collection = mongo[self.collection_name]
        self._collection.create_index("ngrams")
        self._collection.create_index("text")
        self._collection.create_index("field")
        self._collection.create_index(
            [("text", ASCENDING), ("field", ASCENDING)], unique=True
        )

    @staticmethod
    def iter_tokens(items: Iterable[Dict[str, Any]]) -> Iterable[Token]:
        """
        Returns tokens to feed the ngram store
        :param items: Must include keys value and field
        """
        for item in items:
            field = item["field"]
            value = item["value"]
            yield Token.from_field_value(field, value)

    def update(self, tokens: Iterable[Token]):
        """ Rebuild the ngrom index given a list of tokens """
        entries: Dict[Tuple[str, str], Dict[str, Any]] = {}
        for token in tokens:
            key = (token.text, token.field)
            entry = token.as_entry()
            if key in entries and entries[key]["data"] != entry["data"]:
                entries[key]["data"].setdefault("other", [])
                entries[key]["data"]["other"] = entry["data"]
            elif key not in entries:
                entries[key] = entry

        self._collection.drop()
        self._collection.insert_many(list(entries.values()), ordered=False)

    def update_from_store(self, publication_store: PublicationStore):
        """ Rebuild by querying the publication_store """
        field_names = ["year", "authors", "journal", "disciplines", "keywords"]
        distincts = (
            publication_store.get_distinct(field, as_dict=False)
            for field in field_names
        )
        tokens = self.iter_tokens(chain(*distincts))
        self.update(tokens)

    def query(self, search: str, first: int, filters: FilterList) -> List[TokenResult]:
        """
        Perform a fuzzy search in the ngram store.
        Return only `first` top results
        """
        search = search.strip().lower()
        ngrams = get_ngrams(search)

        # jaccard score (intersection over union) as mongodb aggregation
        jaccard_scorer = {
            "$let": {
                "vars": {
                    "intersSize": {"$size": {"$setIntersection": ["$ngrams", ngrams]}},
                    "unionSize": {"$size": {"$setUnion": ["$ngrams", ngrams]}},
                },
                "in": {
                    "$cond": {
                        "if": {"$eq": ["$$unionSize", 0]},
                        "then": 0,
                        "else": {"$divide": ["$$intersSize", "$$unionSize"]},
                    }
                },
            }
        }

        # prefix scorer is fraction of matching characters from the start
        prefix_scorer = {
            "$cond": {
                "if": {"$eq": [{"$substrCP": ["$text", 0, len(search)]}, search]},
                "then": {"$divide": [len(search), {"$strLenCP": "$text"}]},
                "else": 0.0,
            },
        }

        aggregation: List[Dict[str, Any]] = [
            {
                "$match": {
                    "$or": [
                        {"ngrams": {"$in": ngrams}},
                        {"text": {"$regex": f"^{search}"}},
                    ],
                }
            }
        ]

        # exclude active filters
        if not filters.empty:
            filter_exclusion_queries = []
            for field, value in filters.iter_flat(as_dict=False):
                exclusion = Token.from_field_value(field, value).as_field_text()
                filter_exclusion_queries.append(exclusion)

            aggregation += [{"$match": {"$nor": filter_exclusion_queries}}]

        aggregation += [
            {
                "$addFields": {
                    "jaccardScore": jaccard_scorer,
                    "prefixScore": prefix_scorer,
                }
            },
            {
                "$project": {
                    "_id": False,
                    "text": True,
                    "field": True,
                    "data": True,
                    "score": {"$max": ["$jaccardScore", "$prefixScore"]},
                },
            },
            {"$sort": {"score": -1}},
            {"$limit": first},
        ]

        cursor = self._collection.aggregate(aggregation)
        return [TokenResult.from_entry(result) for result in cursor]

    def get_tokens_for_field(self, field: str) -> List[Token]:
        """ Returns all tokens for a field """
        cursor = self._collection.find(
            {"field": field},
            {"_id": False, "text": True, "field": True, "data": True},
        )
        return [Token.from_dict(item) for item in cursor]
