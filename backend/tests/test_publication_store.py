from datetime import datetime
from unittest.mock import patch
import pytest

from ascmonitor.publication_store import (
    PublicationStore,
    assign_cursor,
    encode_cursor,
    decode_cursor,
)


@pytest.fixture
def mendeleur(publications):
    with patch("ascmonitor.mendeleur.Mendeleur") as mendeleur_mock:
        mendeleur_mock.all_documents.return_value = publications
        yield mendeleur_mock


@pytest.fixture
def event_store(mongo):
    with patch("ascmonitor.event_store.EventStore") as event_store_mock:
        yield event_store_mock


@pytest.fixture
def publication_store(mendeleur, event_store, mongo):
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    publication_store.update()
    return publication_store


@pytest.fixture
def publications_response(publications):
    docs = PublicationStore._prepare_for_insert(publications)
    for doc in docs:
        del doc["_id"]
        doc["cursor"] = encode_cursor(doc["cursor"])
    return docs


def test_update(mendeleur, mongo, event_store):
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    publication_store.update()
    mendeleur.all_documents.assert_called_once()
    event_store.put.assert_called()


def test_put(mendeleur, mongo, event_store, publications, publications_response):
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    changes = publication_store.put(publications)
    assert publication_store.get_publications() == publications_response

    created, removed, updated = changes
    assert created == {doc["id"] for doc in publications}
    assert removed == set()
    assert updated == {}


def test_put__ignore_old(publication_store, publications, publications_response):
    changes = publication_store.put(publications)
    assert publication_store.get_publications() == publications_response

    created, removed, updated = changes
    assert created == set()
    assert removed == set()
    assert updated == {}


def test_put__update(publication_store, publications, publications_response):
    updated = [{**publications[0], "year": 2050}, publications[1]]
    expected = [{**publications_response[0], "year": 2050}, publications_response[1]]

    changes = publication_store.put(updated)
    assert publication_store.get_publications() == expected

    created, removed, updated = changes
    assert created == set()
    assert removed == set()
    assert updated == {publications[0]["id"]: {"year": 2050}}


def test_put__delete(publication_store, publications, publications_response):
    changes = publication_store.put([publications[0]])
    assert publication_store.get_publications() == [publications_response[0]]

    created, removed, updated = changes
    assert created == set()
    assert removed == {publications[1]["id"]}
    assert updated == {}


def test_get_by_slug(publication_store, publications, publications_response):
    doc = publications_response[0]
    first_slug = doc["slug"]

    response = publication_store.get_by_slug(first_slug)
    assert response == doc

    # change slug of one publication
    updated = [{**publications[0], "title": "Title triggers new slug"}, publications[1]]
    publication_store.put(updated)
    expected = publication_store.get_by_id(doc["id"])
    new_slug = expected["slug"]

    # publication should be reachable by both slugs now
    assert publication_store.get_by_slug(first_slug) == expected
    assert publication_store.get_by_slug(new_slug) == expected


def test_assign_cursor(publications):
    expected = "2020-01-02T12:00:00$1"
    cursor = assign_cursor(publications[0])["cursor"]
    assert expected == cursor


def test_encode_decode_cursor(publications):
    cursor = "$".join([publications[0]["created"].isoformat(), publications[0]["id"]])

    encoded = encode_cursor(cursor)
    assert encoded == "MjAyMC0wMS0wMlQxMjowMDowMCQx"

    decoded = decode_cursor(encoded)
    assert decoded == cursor


def test_get_publications(publication_store, publications_response):
    fetched = publication_store.get_publications()
    assert fetched == publications_response


def test_get_publications_by_id(publication_store, publications_response):
    ids = [pub["id"] for pub in publications_response]
    assert publication_store.get_by_ids(ids) == publications_response


def test_get_publications__limit(publication_store, publications_response):
    fetched = publication_store.get_publications(first=1)
    assert fetched == [publications_response[0]]


def test_get_publications__cursor(publication_store, publications_response):
    fetched = publication_store.get_publications(
        cursor=publications_response[0]["cursor"]
    )
    assert fetched == [publications_response[1]]


def test_get_publications__filter_authors(publication_store, publications_response):
    filters = {"authors": [publications_response[0]["authors"][0]]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [publications_response[0]]


def test_get_publications__filter_year(publication_store, publications_response):
    filters = {"year": [publications_response[0]["year"]]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == publications_response


def test_get_publications__filter_disciplines(publication_store, publications_response):
    filters = {"disciplines": [publications_response[0]["disciplines"][0]]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [publications_response[0]]


def test_get_publications__filter_unmatched(publication_store, publications_response):
    filters = {"disciplines": ["Invalid"]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == []


def test_get_publications__filter_combination_hit(
    publication_store, publications, publications_response
):
    filters = {
        "disciplines": [publications[0]["disciplines"][0]],
        "keywords": [publications[0]["keywords"][0]],
    }
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [publications_response[0]]


def test_get_publications__filter_combination_multiple(
    publication_store, publications, publications_response
):
    filters = {
        "disciplines": [
            publications[0]["disciplines"][0],
            publications[1]["disciplines"][0],
        ]
    }
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == publications_response


def test_get_publications__filter_combination_exclusion(
    publication_store, publications, publications_response
):
    filters = {
        "disciplines": [publications[0]["disciplines"][0]],
        "keywords": [publications[1]["keywords"][0]],
    }
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == []
