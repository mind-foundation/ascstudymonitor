from unittest.mock import patch
import pytest

from ascmonitor.document_store import (
    DocumentStore,
    assign_cursor,
    encode_cursor,
    decode_cursor,
)


@pytest.fixture
def mendeleur(documents):
    with patch("ascmonitor.mendeleur.Mendeleur") as mendeleur_mock:
        mendeleur_mock.all_documents.return_value = documents
        yield mendeleur_mock


@pytest.fixture
def event_store(mongo):
    with patch("ascmonitor.event_store.EventStore") as event_store_mock:
        yield event_store_mock


@pytest.fixture
def document_store(mendeleur, event_store, mongo):
    document_store = DocumentStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    document_store.update()
    return document_store


@pytest.fixture
def documents_response(documents):
    docs = DocumentStore._prepare_docs_for_insert(documents)
    for doc in docs:
        del doc["_id"]
        doc["cursor"] = encode_cursor(doc["cursor"])
    return docs


def test_update(mendeleur, mongo, event_store):
    document_store = DocumentStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    document_store.update()
    mendeleur.all_documents.assert_called_once()


def test_put(mendeleur, mongo, event_store, documents, documents_response):
    document_store = DocumentStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    document_store.put(documents)
    assert document_store.get_documents() == documents_response


def test_put__ignore_old(document_store, documents, documents_response):
    document_store.put(documents)
    assert document_store.get_documents() == documents_response


def test_put__update(document_store, documents, documents_response):
    updated = [{**documents[0], "year": 2050}, documents[1]]
    expected = [{**documents_response[0], "year": 2050}, documents_response[1]]

    document_store.put(updated)
    assert document_store.get_documents() == expected


def test_put__delete(document_store, documents, documents_response):
    document_store.put([documents[0]])
    assert document_store.get_documents() == [documents_response[0]]


def test_get_by_slug(document_store, documents, documents_response):
    doc = documents_response[0]
    first_slug = doc["slug"]

    response = document_store.get_by_slug(first_slug)
    assert response == doc

    # change slug of one document
    updated = [{**documents[0], "title": "Title triggers new slug"}, documents[1]]
    document_store.put(updated)
    expected = document_store.get_by_id(doc["id"])
    new_slug = expected["slug"]

    # document should be reachable by both slugs now
    assert document_store.get_by_slug(first_slug) == expected
    assert document_store.get_by_slug(new_slug) == expected


def test_assign_cursor(documents):
    expected = "2020-01-02T12:00:00$1"
    cursor = assign_cursor(documents[0])["cursor"]
    assert expected == cursor


def test_encode_decode_cursor(documents):
    cursor = "$".join([documents[0]["created"].isoformat(), documents[0]["id"]])

    encoded = encode_cursor(cursor)
    assert encoded == "MjAyMC0wMS0wMlQxMjowMDowMCQx"

    decoded = decode_cursor(encoded)
    assert decoded == cursor


def test_get_documents(document_store, documents_response):
    fetched = document_store.get_documents()
    assert fetched == documents_response


def test_get_documents__limit(document_store, documents_response):
    fetched = document_store.get_documents(first=1)
    assert fetched == [documents_response[0]]


def test_get_documents__cursor(document_store, documents_response):
    fetched = document_store.get_documents(cursor=documents_response[0]["cursor"])
    assert fetched == [documents_response[1]]


def test_get_documents__filter_authors(document_store, documents_response):
    filters = {"authors": [documents_response[0]["authors"][0]]}
    fetched = document_store.get_documents(filters=filters)
    assert fetched == [documents_response[0]]


def test_get_documents__filter_year(document_store, documents_response):
    filters = {"year": [documents_response[0]["year"]]}
    fetched = document_store.get_documents(filters=filters)
    assert fetched == documents_response


def test_get_documents__filter_disciplines(document_store, documents_response):
    filters = {"disciplines": [documents_response[0]["disciplines"][0]]}
    fetched = document_store.get_documents(filters=filters)
    assert fetched == [documents_response[0]]


def test_get_documents__filter_unmatched(document_store, documents_response):
    filters = {"disciplines": ["Invalid"]}
    fetched = document_store.get_documents(filters=filters)
    assert fetched == []
