"""
Abstract Cache interface for scraper response caching.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    """Abstract Cache interface."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get cached item by key."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set cached item with optional TTL in seconds."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete cached item."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cached entries."""
        pass
