import pytest
from unittest.mock import patch, create_autospec
from humps import camelize

from ariadne.graphql import graphql_sync

from ascmonitor.mendeleur import Mendeleur
from ascmonitor.publication_store import PublicationStore
from ascmonitor.ngram_store import NGramStore
from ascmonitor.event_store import EventStore


@pytest.fixture(scope="package")
def mongo_graphql(real_mongo_connection):
    yield real_mongo_connection["asc-test-graphql"]


@pytest.fixture(scope="package")
def graphql(mendeleur_pkg, mongo_graphql, publications):
    event_store = EventStore(mongo_graphql)
    ngram_store = NGramStore(mongo_graphql)
    publication_store = PublicationStore(
        mendeleur=mendeleur_pkg, mongo=mongo_graphql, event_store=event_store
    )

    with patch.multiple(
        "ascmonitor.globals",
        mendeleur=mendeleur_pkg,
        mongo=mongo_graphql,
        event_store=event_store,
        publication_store=publication_store,
        ngram_store=ngram_store,
    ):
        from ascmonitor.graphql import schema

        def execute_query(query, **variables):
            data = {"query": query, "variables": variables}
            success, result = graphql_sync(schema, data=data, debug=True)

            assert success, f"Query failed: {query}"
            result = result["data"]
            if len(result) == 1:
                result = next(iter(result.values()))

            return result

        result = execute_query("mutation {updatePublications {success}}")
        assert result["success"]

        yield execute_query


@pytest.fixture()
def field_suggestions_query():
    return """
    query($search: String!, $filters: FilterInput) {
        fieldSuggestions(search: $search, first: 5, filters: $filters) {
            value {
              __typename
              ... on Year {
                year: value
                publicationCount
              }
              ... on Author {
                firstName
                lastName
                publicationCount
              }
              ... on Journal {
                value
                publicationCount
              }
              ... on Discipline {
                value
                publicationCount
              }
              ... on Keyword {
                value
                publicationCount
              }
            }
            field
            score
        }
    }
    """


@pytest.fixture()
def publications_query():
    return """
    query($search: String, $filters: FilterInput, $after: String) {
      publications(search: $search, filters: $filters, after: $after) {
        pageInfo {
          hasNextPage
          endCursor
        }

        edges {
          cursor
          score
          node {
            id
            abstract
            authors {
              firstName
              lastName
            }
            created
            disciplines {
              value
            }
            fileAttached
            id
            keywords {
              value
            }
            slug
            journal {
              value
            }
            title
            websites
            year {
              value
            }
          }
        }
      }
    }
    """


@pytest.fixture
def publication_query():
    return """
    query($slug: String!) {
      publication: publicationBySlug(slug: $slug) {
        abstract
        authors {
          firstName
          lastName
        }
        created
        disciplines {
          value
        }
        fileAttached
        id
        keywords {
          value
        }
        slug
        journal {
          value
        }
        title
        websites
        year {
          value
        }
        recommendations(first: 5) {
          score
          publication {
            abstract
            authors {
              firstName
              lastName
            }
            created
            disciplines {
              value
            }
            fileAttached
            id
            keywords {
              value
            }
            slug
            journal {
              value
            }
            title
            websites
            year {
              value
            }
          }
        }
      }
    }
    """


def test_update_publications(graphql):
    result = graphql("mutation {updatePublications {success}}")
    assert result["success"]


def test_get_authors(graphql, publications):
    expected = []
    for pub in publications:
        for author in pub.authors:
            if author not in expected:
                expected.append({**camelize(author.as_dict()), "publicationCount": 1})

    expected.sort(key=lambda a: a["lastName"])

    result = graphql("{authors {firstName, lastName, publicationCount}}")
    result.sort(key=lambda a: a["lastName"])

    assert result == expected


def test_get_publications(graphql, publications_query, publications):
    expected = {
        "edges": [
            {
                "cursor": pub.encoded_cursor,
                "score": None,
                "node": pub.as_gql_response(with_cursor=False, created_as_str=True),
            }
            for pub in publications
        ],
        "pageInfo": {
            "endCursor": publications[-1].encoded_cursor,
            "hasNextPage": False,
        },
    }

    result = graphql(publications_query)
    assert result == expected


def test_get_publications__cursor(graphql, publications_query, publications):
    expected = {
        "edges": [
            {
                "cursor": pub.encoded_cursor,
                "score": None,
                "node": pub.as_gql_response(with_cursor=False, created_as_str=True),
            }
            for pub in publications[1:]
        ],
        "pageInfo": {
            "endCursor": publications[-1].encoded_cursor,
            "hasNextPage": False,
        },
    }

    result = graphql(publications_query, after=publications[0].encoded_cursor)
    assert result == expected


def test_get_publications__search(graphql, publications_query, publications):
    expected = {
        "edges": [
            {
                "cursor": "MTcyNTAwMC8x",
                "score": 1.725,
                "node": pub.as_gql_response(with_cursor=False, created_as_str=True),
            }
            for pub in [publications[0]]
        ],
        "pageInfo": {
            "endCursor": "MTcyNTAwMC8x",
            "hasNextPage": False,
        },
    }

    search = " ".join(publications[0].title.split()[1:-1])
    result = graphql(publications_query, search=search)
    assert result == expected


def test_get_publications__search_cursor(graphql, publications_query, publications):
    expected = {
        "edges": [
            {
                "cursor": "MTA0NzYxOS8y",
                "score": 1.0476190476190477,
                "node": pub.as_gql_response(with_cursor=False, created_as_str=True),
            }
            for pub in [publications[1]]
        ],
        "pageInfo": {
            "endCursor": "MTA0NzYxOS8y",
            "hasNextPage": False,
        },
    }

    search = "common term"
    result = graphql(publications_query, search=search, after="MTA1MDAwMC8x")
    assert result == expected


def test_get_publications__filter(graphql, publications_query, publications):
    expected = {
        "edges": [
            {
                "cursor": pub.encoded_cursor,
                "score": None,
                "node": pub.as_gql_response(with_cursor=False, created_as_str=True),
            }
            for pub in publications[1:]
        ],
        "pageInfo": {
            "endCursor": publications[-1].encoded_cursor,
            "hasNextPage": False,
        },
    }

    filters = {"authors": [publications[-1].authors[0].as_dict()]}
    filters = camelize(filters)
    result = graphql(publications_query, filters=filters)
    assert result == expected


def test_get_publication(graphql, publication_query, publications):
    slug = publications[0].slug
    expected = publications[0].as_gql_response(with_cursor=False, created_as_str=True)

    result = graphql(publication_query, slug=slug)

    assert result["recommendations"]
    del result["recommendations"]
    assert result == expected


def test_get_publications_by_title(graphql, publications):
    query = """
    query($title: String!) {
        publicationsByTitle(title: $title) {
            title
            id
        }
    }
    """
    pub = publications[0]
    expected = [{"title": pub.title, "id": pub.id_}]
    title = pub.title[:6]
    result = graphql(query, title=title)
    assert result == expected


def test_queue__empty(graphql):
    view_queue_query = """
    query($channel: String!) {
      queue(channel: $channel) {
        id
        slug
        title
      }
    }
    """
    result = graphql(view_queue_query, channel="twitter")
    assert result == []


def test_queue__mutate(graphql, publications):
    view_queue_query = """
    query($channel: String!) {
      queue(channel: $channel) {
        id
      }
    }
    """

    append_mutation = """
    mutation($channel: String!, $publication: ID!) {
      appendToQueue(channel: $channel, publication: $publication) {
        success
      }
    }
    """

    down_mutation = """
    mutation($channel: String!, $publication: ID!) {
      moveDownInQueue(channel: $channel, publication: $publication) {
        success
      }
    }
    """

    up_mutation = """
    mutation($channel: String!, $publication: ID!) {
      moveUpInQueue(channel: $channel, publication: $publication) {
        success
      }
    }
    """

    remove_mutation = """
    mutation($channel: String!, $publication: ID!) {
      removeFromQueue(channel: $channel, publication: $publication) {
        success
      }
    }
    """

    ids = [pub.id_ for pub in publications]
    expected = [{"id": pub.id_} for pub in publications]

    assert graphql(view_queue_query, channel="twitter") == []

    assert graphql(append_mutation, channel="twitter", publication=ids[0])["success"]
    assert graphql(view_queue_query, channel="twitter") == [expected[0]]

    assert graphql(append_mutation, channel="twitter", publication=ids[1])["success"]
    assert graphql(view_queue_query, channel="twitter") == expected

    assert graphql(down_mutation, channel="twitter", publication=ids[0])["success"]
    assert graphql(view_queue_query, channel="twitter") == expected[::-1]

    assert graphql(up_mutation, channel="twitter", publication=ids[0])["success"]
    assert graphql(view_queue_query, channel="twitter") == expected

    assert graphql(up_mutation, channel="twitter", publication=ids[0])["success"]
    assert graphql(view_queue_query, channel="twitter") == expected

    assert graphql(remove_mutation, channel="twitter", publication=ids[0])["success"]
    assert graphql(view_queue_query, channel="twitter") == [expected[1]]

    assert graphql(remove_mutation, channel="twitter", publication=ids[1])["success"]
    assert graphql(view_queue_query, channel="twitter") == []


def test_field_suggestions(graphql, mongo_graphql, field_suggestions_query):
    expected = [
        {
            "value": {
                "__typename": "Keyword",
                "value": "Free Energy Principle",
                "publicationCount": 1,
            },
            "field": "keywords",
            "score": 1 / 5,
        },
        {
            "value": {
                "__typename": "Keyword",
                "value": "Predictive Coding",
                "publicationCount": 1,
            },
            "field": "keywords",
            "score": 2 / 15,
        },
    ]
    result = graphql(field_suggestions_query, search="pred princ")
    assert result == expected


def test_field_suggestions__exclude(graphql, mongo_graphql, field_suggestions_query):
    expected = [
        {
            "value": {
                "__typename": "Keyword",
                "value": "Free Energy Principle",
                "publicationCount": 1,
            },
            "field": "keywords",
            "score": 1 / 5,
        },
    ]
    result = graphql(
        field_suggestions_query,
        search="pred princ",
        filters={"keywords": ["Predictive Coding"]},
    )
    assert result == expected


def test_field_suggestions__authors(graphql, field_suggestions_query):
    expected = [
        {
            "value": {
                "__typename": "Author",
                "firstName": "Karl",
                "lastName": "Friston",
                "publicationCount": 1,
            },
            "field": "authors",
            "score": 5 / 7,
        },
    ]
    result = graphql(
        field_suggestions_query,
        search="friston",
    )
    assert result == expected


def test_field_suggestions__exclude_authors(graphql, field_suggestions_query):
    result = graphql(
        field_suggestions_query,
        search="friston",
        filters={"authors": [{"firstName": "Karl", "lastName": "Friston"}]},
    )
    assert not result
