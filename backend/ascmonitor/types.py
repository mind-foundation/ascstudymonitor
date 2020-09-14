""" Domain-specific types """
from typing import Any, List, Dict, Optional, Union

PublicationType = Dict[str, Any]
PublicationsType = List[PublicationType]

# Filters are mapping from field name to list of included items.
# The list may be None to play nicely with GraphQL
FilterItem = Union[str, Dict[str, str]]
FilterList = Dict[str, Optional[List[FilterItem]]]
