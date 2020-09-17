import pytest

from ascmonitor.ngram_store import get_ngrams, NGramStore, Token, TokenResult


@pytest.fixture
def ngram_store(real_mongo):
    return NGramStore(real_mongo)


@pytest.fixture
def tokens():
    return [
        Token(text="therapy", field="keywords", data={"value": "Therapy"}),
        Token(
            text="David Nutt",
            field="authors",
            data={"value": {"firstName": "David", "lastName": "Nutt"}},
        ),
    ]


def test_get_ngrams():
    token = "Lysergic acid"
    expected = ["lys", "yse", "ser", "erg", "rgi", "gic", "aci", "cid"]
    assert get_ngrams(token) == expected


def test_get_ngrams__special_char():
    token = "Δ9-THC"
    expected = ["δ9t", "9th", "thc"]
    assert get_ngrams(token) == expected


def test_token_as_entry(tokens):
    # test serialization
    entries = [
        dict(
            text="therapy",
            field="keywords",
            data={"value": "Therapy"},
            ngrams=["the", "her", "era", "rap", "apy"],
        ),
        dict(
            text="David Nutt",
            field="authors",
            data={"value": {"firstName": "David", "lastName": "Nutt"}},
            ngrams=["dav", "avi", "vid", "nut", "utt"],
        ),
    ]
    assert [token.as_entry() for token in tokens] == entries

    # test parsing
    results = [TokenResult.from_entry({**entry, "score": 3.14}) for entry in entries]
    expected = [
        TokenResult(text=token.text, field=token.field, data=token.data, score=3.14)
        for token in tokens
    ]
    assert results == expected


def test_update(ngram_store, tokens):
    expected = [token.as_entry() for token in tokens]

    ngram_store.update(tokens)
    entries = list(ngram_store._collection.find({}, {"_id": False}))
    assert entries == expected

    # second update wont change the data
    ngram_store.update(tokens)
    entries = list(ngram_store._collection.find({}, {"_id": False}))
    assert entries == expected


def test_query(ngram_store, tokens):
    query = "terapy"
    expected_ngrams = ["ter", "era", "rap", "apy"]
    assert get_ngrams(query) == expected_ngrams

    inters = set(expected_ngrams) & set(tokens[0].ngrams)
    union = set(expected_ngrams) | set(tokens[0].ngrams)
    exp_score = len(inters) / len(union)

    ngram_store.update(tokens)
    result = ngram_store.query(query, first=1)[0]
    assert result.text == "therapy"
    assert abs(result.score - exp_score) < 0.001


def test_get_tokens_for_field(ngram_store, tokens):
    ngram_store.update(tokens)

    expected = [tokens[0].as_entry()]
    del expected[0]["ngrams"]

    assert ngram_store.get_tokens_for_field("keywords") == expected
