import pytest

from ascmonitor.document_cache import DocumentCache, Changes


def assert_doc_id_equal(a, b):
    assert a["id"] == b["id"]


def assert_changes_equal(changes, created=None, updated=None, removed=None):
    """ Compare changes by few fields only """
    sort_key = lambda d: d["id"]
    for change, expected in zip(
        (changes.created, changes.updated, changes.removed), (created, updated, removed)
    ):
        if expected is None:
            assert change == []
        else:
            for a, b in zip(
                sorted(change, key=sort_key), sorted(expected, key=sort_key)
            ):
                assert_doc_id_equal(a, b)


@pytest.fixture
def document_cache(mongo, documents):
    source_fn = lambda: documents
    return DocumentCache(mongo=mongo, source_fn=source_fn, expires=10)


def test_put(document_cache, documents):
    changes = document_cache.put(documents)
    assert_changes_equal(changes, created=documents)


def test_put__ignore_old(document_cache, documents):
    _ = document_cache.put(documents)
    changes = document_cache.put(documents)
    assert_changes_equal(changes)


def test_put__update(document_cache, documents):
    _ = document_cache.put(documents)
    updated = [{**documents[0], "title": "New title"}, documents[1]]
    changes = document_cache.put(updated)
    assert_changes_equal(changes, updated=[updated[0]])
    assert changes.updated[0]["title"] == updated[0]["title"]


def test_put__delete(document_cache, documents):
    _ = document_cache.put(documents)
    changes = document_cache.put([documents[0]])
    assert_changes_equal(changes, removed=[documents[1]])


def test_slugs(document_cache, documents):
    document_cache.put(documents)
    first_slug = documents[0]["slug"]
    doc = document_cache.get_by_slug(first_slug)
    assert doc == documents[0]

    # change slug of one document
    new_slug = "new-slug"
    updated = [{**documents[0], "slug": new_slug}, documents[1]]
    document_cache.put(updated)

    # document should be reachable by both slugs now
    assert document_cache.get_by_slug(first_slug) == updated[0]
    assert document_cache.get_by_slug(new_slug) == updated[0]
