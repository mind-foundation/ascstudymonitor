""" ASC Study Monitor Infrastructure """
__version__ = "2.0.0"

from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {"format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",}
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

import sentry_sdk

sentry_sdk.init("https://91d6a27d4de14deba93bac991e05185f@sentry.io/1661534")

# some global types
from typing import Any, List, Dict

DocumentType = Dict[str, Any]
DocumentsType = List[DocumentType]
