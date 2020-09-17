"""
A mongodb powered fuzzy string search engine.
Strings are compared by comparing their n-gram sets.
"""

from dataclasses import dataclass
import re
from typing import Any, Dict, List, Optional

from nltk import everygrams
from pymongo.database import Database

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


@dataclass
class Token:
    """
    A token which might be associated with a field.
    Text must be a string, but allows storing additional data.
    """

    text: str
    field: str
    data: Optional[Dict[str, Any]]

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


@dataclass
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


class NGramStore:
    """ Fuzzy string search engine """

    collection_name = "ngram_index"

    def __init__(self, mongo: Database):
        self._collection = mongo[self.collection_name]
        self._collection.create_index("ngrams")
        self._collection.create_index("field")

    def update(self, tokens: List[Token]):
        """ Rebuild the ngrom index given a list of tokens """
        entries = [token.as_entry() for token in tokens]
        self._collection.drop()
        self._collection.insert_many(entries, ordered=False)

    def query(self, search: str, first: int) -> List[TokenResult]:
        """
        Perform a fuzzy search in the ngram store.
        Return only `first` top results
        """
        ngrams = get_ngrams(search)

        # jaccard score (intersection over union) as mongodb aggregation
        jaccard_scorer = {
            "$divide": [
                {"$size": {"$setIntersection": ["$ngrams", ngrams]}},
                {"$size": {"$setUnion": ["$ngrams", ngrams]}},
            ]
        }

        aggregation = [
            {"$match": {"ngrams": {"$in": ngrams}}},
            {
                "$project": {
                    "_id": False,
                    "text": True,
                    "field": True,
                    "data": True,
                    "score": jaccard_scorer,
                }
            },
            {"$sort": {"score": -1}},
            {"$limit": first},
        ]

        return [
            TokenResult.from_entry(result)
            for result in self._collection.aggregate(aggregation)
        ]

    def get_tokens_for_field(self, field: str) -> List[Dict[str, Any]]:
        """ Returns all tokens for a field """
        return list(
            self._collection.find(
                {"field": field},
                {"_id": False, "text": True, "field": True, "data": True},
            )
        )
