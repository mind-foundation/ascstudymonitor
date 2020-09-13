""" Domain-specific types """
from typing import Any, List, Dict, Optional, Union

DocumentType = Dict[str, Any]
DocumentsType = List[DocumentType]

# Filters are mapping from field name to list of included items.
# The list may be None to play nicely with GraphQL
FilterItem = Union[str, Dict[str, str]]
FilterList = Dict[str, Optional[List[FilterItem]]]
