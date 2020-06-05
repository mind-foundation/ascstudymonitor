""" ASC Study Monitor Infrastructure """
__version__ = "2.0.0"

from logging.config import dictConfig
from ascmonitor.config import development

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
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
        "root": {"level": "DEBUG" if development else "INFO", "handlers": ["wsgi"]},
    }
)

if not development:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        "https://91d6a27d4de14deba93bac991e05185f@sentry.io/1661534",
        integrations=[FlaskIntegration()],
    )

# some global types
from typing import Any, List, Dict

DocumentType = Dict[str, Any]
DocumentsType = List[DocumentType]
