"""
HTTP client abstractions and implementations.
"""

from resumesh_scrapers.core.http.base import BaseHttpClient
from resumesh_scrapers.core.http.httpx_client import HttpxHttpClient

__all__ = ["BaseHttpClient", "HttpxHttpClient"]
