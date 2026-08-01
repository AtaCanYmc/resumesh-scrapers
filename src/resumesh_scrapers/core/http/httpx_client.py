"""
HTTPX-backed asynchronous HTTP client implementation.
"""

from typing import Any, Optional
import httpx
from resumesh_scrapers.core.http.base import BaseHttpClient
from resumesh_scrapers.exceptions import NetworkError, RateLimitError


class HttpxHttpClient(BaseHttpClient):
    """Asynchronous HTTP Client wrapping HTTPX."""

    def __init__(
        self,
        headers: Optional[dict[str, str]] = None,
        timeout: float = 15.0,
        follow_redirects: bool = True,
    ):
        default_headers = {
            "User-Agent": "ResuMesh-Scrapers/1.0 (+https://github.com/AtaCanYmc/resumesh-scrapers)",
            "Accept": "application/json, text/html, application/xhtml+xml, */*",
        }
        if headers:
            default_headers.update(headers)

        self._client = httpx.AsyncClient(
            headers=default_headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
        )

    async def get(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        try:
            response = await self._client.get(url, headers=headers, params=params, **kwargs)
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded for URL: " + url)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded") from e
            raise NetworkError(f"HTTP Error {e.response.status_code}: {e}") from e
        except httpx.RequestError as e:
            raise NetworkError(f"Network Request Error: {e}") from e

    async def post(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        try:
            response = await self._client.post(url, headers=headers, json=json, data=data, **kwargs)
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded for URL: " + url)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded") from e
            raise NetworkError(f"HTTP Error {e.response.status_code}: {e}") from e
        except httpx.RequestError as e:
            raise NetworkError(f"Network Request Error: {e}") from e

    async def close(self) -> None:
        await self._client.aclose()
