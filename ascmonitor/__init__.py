""" ASC Study Monitor Infrastructure """
__version__ = "2.0.0"

import sentry_sdk

sentry_sdk.init("https://91d6a27d4de14deba93bac991e05185f@sentry.io/1661534")

# some global types
from typing import Any, List, Dict

DocumentType = Dict[str, Any]
DocumentsType = List[DocumentType]
