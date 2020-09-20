from dataclasses import replace
from datetime import datetime
from unittest.mock import patch
import pytest

from ascmonitor.publication_store import PublicationStore


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
def publication_store_real(mendeleur, event_store, real_mongo):
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=real_mongo, event_store=event_store
    )
    publication_store.update()
    return publication_store


def test_update(mendeleur, mongo, event_store):
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    publication_store.update()
    mendeleur.all_documents.assert_called_once()
    event_store.put.assert_called()


def test_put(mendeleur, mongo, event_store, publications):
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    changes = publication_store.put(publications)
    assert publication_store.get_publications() == [
        replace(pub, _cursor=pub.cursor) for pub in publications
    ]

    created, removed, updated = changes
    assert created == {pub.id_ for pub in publications}
    assert removed == set()
    assert updated == {}


def test_put__ignore_old(publication_store, publications):
    changes = publication_store.put(publications)
    assert publication_store.get_publications() == [
        replace(pub, _cursor=pub.cursor) for pub in publications
    ]

    created, removed, updated = changes
    assert created == set()
    assert removed == set()
    assert updated == {}


def test_put__update(publication_store, publications):
    updated = [replace(publications[0], year=2050), publications[1]]

    changes = publication_store.put(updated)
    assert publication_store.get_publications() == [
        replace(pub, _cursor=pub.cursor) for pub in updated
    ]

    created, removed, updated = changes
    assert created == set()
    assert removed == set()
    assert updated == {publications[0].id_: {"year": 2050}}


def test_put__delete(publication_store, publications):
    changes = publication_store.put([publications[0]])
    assert publication_store.get_publications() == [
        replace(publications[0], _cursor=publications[0].cursor)
    ]

    created, removed, updated = changes
    assert created == set()
    assert removed == {publications[1].id_}
    assert updated == {}


def test_get_by_slug(publication_store, publications):
    pub = publications[0]
    first_slug = pub.slug

    response = publication_store.get_by_slug(first_slug)
    assert response == pub

    # change slug of one publication
    updated = [
        replace(publications[0], title="Title triggers new slug"),
        publications[1],
    ]
    publication_store.put(updated)
    expected = publication_store.get_by_id(pub.id_)
    new_slug = expected.slug

    # publication should be reachable by both slugs now
    assert publication_store.get_by_slug(first_slug) == expected
    assert publication_store.get_by_slug(new_slug) == expected


def test_get_publications(publication_store, publications):
    fetched = publication_store.get_publications()
    assert fetched == [replace(pub, _cursor=pub.cursor) for pub in publications]


def test_get_publications_by_id(publication_store_real, publications):
    ids = [pub.id_ for pub in publications[::-1]]
    pubs = publication_store_real.get_by_ids(ids)
    assert [pub.id_ for pub in pubs] == ids


def test_get_publications__limit(publication_store, publications):
    fetched = publication_store.get_publications(first=1)
    assert fetched == [replace(publications[0], _cursor=publications[0].cursor)]


def test_get_publications__cursor(publication_store, publications):
    fetched = publication_store.get_publications(cursor=publications[0].encoded_cursor)
    assert fetched == [replace(publications[1], _cursor=publications[1].cursor)]


def test_get_publications__filter_authors(publication_store, publications):
    filters = {"authors": [publications[0].authors[0].as_dict()]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [replace(publications[0], _cursor=publications[0].cursor)]


def test_get_publications__filter_year(publication_store, publications):
    filters = {"year": [publications[0].year]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [replace(pub, _cursor=pub.cursor) for pub in publications]


def test_get_publications__filter_disciplines(publication_store, publications):
    filters = {"disciplines": [publications[0].disciplines[0]]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [replace(publications[0], _cursor=publications[0].cursor)]


def test_get_publications__filter_unmatched(publication_store):
    filters = {"disciplines": ["Invalid"]}
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == []


def test_get_publications__filter_combination_hit(publication_store, publications):
    filters = {
        "disciplines": [publications[0].disciplines[0]],
        "keywords": [publications[0].keywords[0]],
    }
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [replace(publications[0], _cursor=publications[0].cursor)]


def test_get_publications__filter_combination_multiple(publication_store, publications):
    filters = {
        "disciplines": [
            publications[0].disciplines[0],
            publications[1].disciplines[0],
        ]
    }
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == [replace(pub, _cursor=pub.cursor) for pub in publications]


def test_get_publications__filter_combination_exclusion(
    publication_store, publications
):
    filters = {
        "disciplines": [publications[0].disciplines[0]],
        "keywords": [publications[1].keywords[0]],
    }
    fetched = publication_store.get_publications(filters=filters)
    assert fetched == []


def test_get_publications__search(publication_store_real, publications):
    fetched = publication_store_real.get_publications(
        search="formal statement equilibrium"
    )
    assert len(fetched) == 1
    assert replace(fetched[0], _cursor=None, score=None) == publications[1]
    assert fetched[0].cursor == "1578947/2"
    assert fetched[0].score == pytest.approx(1.578947)


def test_get_publications__search_pagination(publication_store_real, publications):
    abstract = "This is a testing abstract with some infos."
    pubs = [replace(pub, abstract=abstract) for pub in publications]
    publication_store_real.put(pubs)

    # first page
    fetched = publication_store_real.get_publications(
        search="testing abstract", first=1
    )
    assert len(fetched) == 1
    assert replace(fetched[0], _cursor=None, score=None) == pubs[1]
    assert fetched[0]._cursor is not None

    # second page
    fetched = publication_store_real.get_publications(
        search="testing abstract", first=1, cursor=fetched[0].encoded_cursor
    )
    assert len(fetched) == 1
    assert replace(fetched[0], _cursor=None, score=None) == pubs[0]
