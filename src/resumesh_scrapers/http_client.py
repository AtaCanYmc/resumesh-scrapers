import logging
from typing import Dict, Type

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from resumesh_scrapers.exceptions import ScraperError

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def fetch_url(
    url: str,
    headers: Dict[str, str] | None = None,
    timeout: float = 15.0,
    follow_redirects: bool = False,
    error_class: Type[ScraperError] = ScraperError,
    platform_name: str = "PLATFORM",
) -> httpx.Response:
    """
    Standardized helper to fetch a URL with tenacity retry, logging, and error mapping.

    Args:
        url: The URL to request.
        headers: Dict of HTTP headers to include in the request.
        timeout: Timeout in seconds.
        follow_redirects: Whether to follow HTTP redirects.
        error_class: The ScraperError subclass to raise upon failure.
        platform_name: The platform name used in log messages and exceptions.

    Returns:
        The successful httpx.Response object.

    Raises:
        error_class: If a network error occurs or the response status code is not 200.
    """
    logger.debug("[%s] GET request to url=%s", platform_name, url)
    try:
        async with httpx.AsyncClient(
            timeout=timeout, follow_redirects=follow_redirects
        ) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise error_class(
            f"Network error while fetching {platform_name} data: {exc}"
        ) from exc

    if response.status_code != 200:
        raise error_class(
            f"{platform_name} API returned HTTP {response.status_code}."
            f" Response: {response.text[:300]}",
            status_code=response.status_code,
        )

    return response
