import os
import random
import shutil
from subprocess import Popen
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from dateutil.parser import parse as parse_datetime
from mongomock import MongoClient as MongoMock
from pymongo import MongoClient

# setup environment for testing
os.environ["ASC_TESTING"] = "True"
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

from ascmonitor.event_store import EventStore
from ascmonitor.ngram_store import NGramStore
from ascmonitor.publication import Publication
from ascmonitor.publication_store import PublicationStore

mongodb = None


@pytest.fixture(autouse=True, scope="session")
def mongodb_server():
    """ Launches a real mongo server on port 27018 """
    global mongodb
    with TemporaryDirectory() as tmpdir, open(os.devnull, "wb") as devnull:
        mongodb = Popen(
            ["mongod", "--dbpath", tmpdir, "--port", "27018"],
            stdout=devnull,
            stderr=devnull,
        )
        yield
        mongodb.kill()


def pytest_sessionfinish(session, exitstatus):
    """ Ensure mongodb is shut down """
    global mongodb
    if mongodb is not None:
        mongodb.kill()


@pytest.fixture()
def mongo():
    return MongoMock()["asc-test"]


@pytest.fixture(scope="session")
def real_mongo_connection(mongodb_server):
    mongo = MongoClient(
        host="localhost", port=27018, connectTimeoutMS=5000, socketTimeoutMS=1000
    )
    yield mongo


@pytest.fixture()
def real_mongo(real_mongo_connection):
    yield real_mongo_connection["asc-test"]
    real_mongo_connection.drop_database("asc-test")


@pytest.fixture(scope="session")
def publications():
    pubs = [
        {
            "title": "MDMA-assisted PTSD Therapy",
            "authors": [{"first_name": "Rick", "last_name": "Doblin"}],
            "year": 2020,
            "journal": "ASC Journal",
            "websites": ["https://example.com"],
            "id": "1",
            "created": parse_datetime("2020-01-02T12:00:00.000"),
            "file_attached": False,
            "abstract": (
                "We are studying whether MDMA-assisted psychotherapy "
                "can help heal the psychological and emotional damage caused by "
                "sexual assault, war, violent crime, and other traumas. Common term."
            ),
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
            "abstract": (
                "The free energy principle is a formal statement "
                "that explains how living and non-living systems remain "
                "in non-equilibrium steady-states by restricting themselves "
                "to a limited number of states. Common term."
            ),
            "disciplines": ["Neuroscience"],
            "keywords": [
                "Free Energy Principle",
                "Variational Inference",
                "Predictive Coding",
            ],
        },
    ]
    return [Publication.from_dict(pub) for pub in pubs]


@pytest.fixture(scope="package")
def mendeleur_pkg(publications):
    with patch("ascmonitor.mendeleur.Mendeleur") as mendeleur_mock:
        mendeleur_mock.all_documents.return_value = publications
        yield mendeleur_mock


@pytest.fixture()
def mendeleur(publications):
    with patch("ascmonitor.mendeleur.Mendeleur") as mendeleur_mock:
        mendeleur_mock.all_documents.return_value = publications
        yield mendeleur_mock


@pytest.fixture
def event_store_mock(mongo):
    with patch("ascmonitor.event_store.EventStore") as event_store_mock:
        yield event_store_mock


@pytest.fixture
def event_store(mongo):
    return EventStore(mongo)


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


@pytest.fixture
def ngram_store(real_mongo):
    return NGramStore(real_mongo)
