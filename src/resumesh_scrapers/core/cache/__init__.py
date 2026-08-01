"""
Cache layer abstractions and memory implementations.
"""

from resumesh_scrapers.core.cache.base import BaseCache
from resumesh_scrapers.core.cache.memory import InMemoryCache

__all__ = ["BaseCache", "InMemoryCache"]
