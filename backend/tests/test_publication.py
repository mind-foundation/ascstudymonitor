from dateutil.parser import parse as parse_datetime
import pytest

from ascmonitor.publication import Publication


def test_as_gql_response(publications):
    expected = {
        "title": "MDMA-assisted PTSD Therapy",
        "authors": [{"firstName": "Rick", "lastName": "Doblin"}],
        "year": {"value": 2020},
        "journal": {"value": "ASC Journal"},
        "websites": ["https://example.com"],
        "id": "1",
        "created": parse_datetime("2020-01-02T12:00:00.000"),
        "fileAttached": False,
        "abstract": publications[0].abstract,
        "disciplines": [{"value": "Psychiatry"}],
        "keywords": [{"value": "therapy"}, {"value": "MDMA"}, {"value": "PTSD"}],
        "cursor": "MjAyMC0wMS0wMlQxMjowMDowMC8x",
        "slug": "mdma-assisted-ptsd-therapy-1",
    }
    assert publications[0].as_gql_response() == expected


def test_cursor(publications):
    expected = "2020-01-02T12:00:00/1"
    assert publications[0].cursor == expected


def test_encode_decode_cursor(publications):
    cursor = "/".join([publications[0].created.isoformat(), publications[0].id_])

    encoded = publications[0].encoded_cursor
    assert encoded == "MjAyMC0wMS0wMlQxMjowMDowMC8x"

    decoded = Publication.decode_cursor(encoded)
    assert decoded == cursor
