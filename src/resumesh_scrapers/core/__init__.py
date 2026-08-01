"""
Core abstractions and utilities for resumesh-scrapers.
"""

from resumesh_scrapers.core.auth import (
    BaseCredentialProvider,
    EnvCredentialProvider,
    StaticCredentialProvider,
)
from resumesh_scrapers.core.cache import BaseCache, InMemoryCache
from resumesh_scrapers.core.http import BaseHttpClient, HttpxHttpClient
from resumesh_scrapers.core.plugin import ProviderRegistry, registry
from resumesh_scrapers.core.resilience import RateLimiter

__all__ = [
    "BaseHttpClient",
    "HttpxHttpClient",
    "RateLimiter",
    "BaseCache",
    "InMemoryCache",
    "BaseCredentialProvider",
    "EnvCredentialProvider",
    "StaticCredentialProvider",
    "ProviderRegistry",
    "registry",
]
