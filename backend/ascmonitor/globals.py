""" Global state for running app """

import os

from pymongo import MongoClient

from ascmonitor.config import (
    mendeley_authinfo,
    mendeley_group_id,
    mongo_config,
    mongo_db,
)
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur, MendeleyAuthInfo
from ascmonitor.ngram_store import NGramStore
from ascmonitor.publication_store import PublicationStore

if "ASC_TESTING" not in os.environ:
    mendeleur = Mendeleur(MendeleyAuthInfo(**mendeley_authinfo), mendeley_group_id)
    mongo = MongoClient(**mongo_config)[mongo_db]
    event_store = EventStore(mongo)
    publication_store = PublicationStore(
        mendeleur=mendeleur, mongo=mongo, event_store=event_store
    )
    ngram_store = NGramStore(mongo=mongo)
else:
    mendeleur = None  # type: ignore
    mongo = None  # type: ignore
    event_store = None  # type: ignore
    publication_store = None  # type: ignore
    ngram_store = None  # type: ignore
