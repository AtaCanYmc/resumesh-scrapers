"""
In-memory cache implementation with TTL support.
"""

import time
from typing import Any, Optional

from resumesh_scrapers.core.cache.base import BaseCache


class InMemoryCache(BaseCache):
    """In-memory Key-Value store with TTL expiry."""

    def __init__(self, default_ttl_seconds: int = 300):
        self.default_ttl = default_ttl_seconds
        self._store: dict[str, tuple[Any, Optional[float]]] = {}

    async def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        value, expiry = self._store[key]
        if expiry is not None and time.monotonic() > expiry:
            del self._store[key]
            return None
        return value

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expiry = (time.monotonic() + ttl) if ttl > 0 else None
        self._store[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def clear(self) -> None:
        self._store.clear()
