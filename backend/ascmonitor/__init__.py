""" ASC Study Monitor Infrastructure """
# pylint: disable=wrong-import-position,wrong-import-order
__version__ = "3.0.0"

from logging.config import dictConfig
from ascmonitor.config import development

# dictConfig(
#     {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "default": {
#                 "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
#             }
#         },
#         "handlers": {
#             "wsgi": {
#                 "class": "logging.StreamHandler",
#                 "stream": "ext://flask.logging.wsgi_errors_stream",
#                 "formatter": "default",
#             }
#         },
#         "root": {"level": "DEBUG" if development else "INFO", "handlers": ["wsgi"]},
#     }
# )
