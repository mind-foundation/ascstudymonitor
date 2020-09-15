import os
import shutil
import pytest

from dateutil.parser import parse as parse_datetime
from mongomock import MongoClient

# setup environment for testing
os.environ["FLASK_ENV"] = "development"
os.environ["POST_SECRET_TOKEN"] = "post_secret_token_test"
os.environ["MENDELEY_CLIENT_ID"] = "test"
os.environ["MENDELEY_CLIENT_SECRET"] = "xxx"
os.environ["MENDELEY_REDIRECT_URI"] = "http://example.com"
os.environ["MENDELEY_USER"] = "xxx"
os.environ["MENDELEY_PASSWORD"] = "xxx"
os.environ["TWITTER_API_KEY"] = "xxx"
os.environ["TWITTER_API_SECRET"] = "xxx"
os.environ["TWITTER_ACCESS_TOKEN"] = "xxx"
os.environ["TWITTER_ACCESS_SECRET"] = "xxx"


@pytest.fixture
def mongo():
    return MongoClient()["asc-test"]


@pytest.fixture
def publications():
    return [
        {
            "title": "MDMA-assisted PTSD Therapy",
            "authors": [{"first_name": "Rick", "last_name": "Doblin"}],
            "year": 2020,
            "journal": "ASC Journal",
            "websites": ["https://example.com"],
            "id": "1",
            "created": parse_datetime("2020-01-02T12:00:00.000"),
            "file_attached": False,
            "abstract": "First abstract",
            "disciplines": ["Psychiatry"],
            "keywords": ["therapy", "MDMA", "PTSD"],
        },
        {
            "title": "Free Energy Principle",
            "authors": [{"first_name": "Karl", "last_name": "Friston"}],
            "year": 2020,
            "journal": "ASC Journal",
            "websites": ["https://example.com"],
            "id": "2",
            "created": parse_datetime("2020-01-01T12:00:00.000"),
            "file_attached": True,
            "abstract": "Second abstract",
            "disciplines": ["Neuroscience"],
            "keywords": [
                "Free Energy Principle",
                "Variational Inference",
                "Predictive Coding",
            ],
        },
    ]
