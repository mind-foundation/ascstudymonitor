"""
Build and persists an index on the publications
for full text search and filtering
"""

import os
from typing import Dict, List, Optional

from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh.fields import Schema, ID, TEXT, KEYWORD, NUMERIC
from whoosh.qparser import MultifieldParser

from ascmonitor.config import search_index_path
from ascmonitor.types import PublicationType, PublicationsType


class SearchEngine:
    """ Provides full text search for publications """

    # To be refined once we have a frontend for the search
    schema = Schema(
        id=ID(unique=True, stored=True),
        title=TEXT(field_boost=3.0),
        authors=KEYWORD(lowercase=True, scorable=True, field_boost=2.0),
        journal=ID(field_boost=2.0),
        keywords=KEYWORD(lowercase=True, scorable=True, commas=True, field_boost=2.0),
        disciplines=KEYWORD(
            lowercase=True, scorable=True, commas=True, field_boost=2.0
        ),
        abstract=TEXT(analyzer=StemmingAnalyzer()),
        year=NUMERIC(),
    )
    searchable_fields = [
        "title",
        "authors",
        "journal",
        "keywords",
        "disciplines",
        "abstract",
        "year",
    ]

    def __init__(self, publications: PublicationsType):
        """ Initialize the search engine with publications """
        self.query_parser = MultifieldParser(self.searchable_fields, schema=self.schema)
        self.build_index(publications)

    def _init_index(self):
        """ Initialize an empty index """
        os.makedirs(search_index_path, exist_ok=True)
        return create_in(search_index_path, self.schema)

    def build_index(self, publications: PublicationsType):
        """
        Build a new index for the publications.
        Raises exception if multiple instances of this function
        run at the same time.
        """
        index = self._init_index()
        writer = index.writer()
        for pub in publications:
            pub = self.transform_publication(pub)
            writer.add_document(**pub)
        writer.commit()
        self.index = index

    def search(self, query: str, limit: Optional[int] = None) -> List[str]:
        """ Search the index and return a list of document ids """
        parsed_query = self.query_parser.parse(query)
        with self.index.searcher() as searcher:
            results = searcher.search(parsed_query, limit=limit)
        return [result["id"] for result in results]

    def transform_publication(self, publication: PublicationType) -> Dict[str, str]:
        """
        Transforms a publication to a search friendly format
        """
        return {
            "id": publication["id"],
            "title": publication["title"],
            "authors": " ".join(
                self._join_author(author) for author in publication["authors"]
            ),
            "journal": publication["journal"],
            "keywords": ",".join(publication["keywords"]),
            "disciplines": ",".join(publication["disciplines"]),
            "abstract": publication["abstract"],
            "year": publication["year"],
        }

    @staticmethod
    def _join_author(author: Dict[str, Optional[str]]) -> str:
        """ Joins a structured author name into a plain string """
        joined = ""
        for name_field in ("firstName", "lastName"):
            if name_field in author:
                # verbose to make mypy happy
                name = author[name_field]
                if name is not None:
                    joined += name
        return joined
