"""
Abstract HTTP Client interface for decoupled network operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseHttpClient(ABC):
    """Abstract HTTP client interface."""

    @abstractmethod
    async def get(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Send asynchronous GET request."""
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """Send asynchronous POST request."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close client sessions and resources."""
        pass
