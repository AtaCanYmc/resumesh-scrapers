"""
Dev.to Scraper Service
========================
Fetches the user's articles using Dev.to's public REST API
and returns them as ``ScrapedArticle`` models.

Usage:
    from resumesh_scrapers import DevToScraperService

    scraper = DevToScraperService()
    articles = await scraper.fetch_data(
        username="atacanymc",
        api_key="your_devto_api_key",   # optional
    )

API Reference:
    GET https://dev.to/api/articles?username={username}
    Docs: https://developers.forem.com/api/v1#tag/articles/operation/getArticles

To obtain an API key:
    https://dev.to/settings/extensions → "DEV Community API Keys"
"""

import logging
import re
from datetime import datetime, timezone

from resumesh_scrapers.core.client import fetch_url
from resumesh_scrapers.exceptions import DevToScraperError
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle
from resumesh_scrapers.platforms.base import IScraperService

logger = logging.getLogger(__name__)

_DEVTO_API_BASE = "https://dev.to/api"
_DEFAULT_TIMEOUT = 15.0
_DEFAULT_PER_PAGE = 1000


class DevToScraperService(IScraperService):
    """
    Service that fetches article data using the Dev.to REST API.
    """

    @staticmethod
    def _build_headers(api_key: str | None = None) -> dict[str, str]:
        """
        Creates HTTP headers for Dev.to API.

        Args:
            api_key: Dev.to API key (optional).
                     If provided, rate limits are increased
                     and private articles are included.

        Returns:
            Header dict. Accept header is always included.
        """
        headers: dict[str, str] = {
            "Accept": "application/vnd.forem.api-v1+json",
        }
        if api_key:
            headers["api-key"] = api_key
        return headers

    @staticmethod
    def _parse_article(raw: dict) -> ScrapedArticle:
        """
        Converts the raw article dict from Dev.to API to ``ScrapedArticle``.

        Args:
            raw: Single article object returned by Dev.to API.

        Returns:
            A ``ScrapedArticle`` object.
        """
        published_at: datetime | None = None
        if raw.get("published_at"):
            try:
                published_at = datetime.strptime(raw["published_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except ValueError:
                # Some dates may have milliseconds or timezone offset
                logger.debug(
                    "[DEV_TO] Could not parse date '%s' for article id=%s, using now()",
                    raw.get("published_at"),
                    raw.get("id"),
                )
                published_at = datetime.now(timezone.utc)

        return ScrapedArticle(
            title=raw["title"],
            summary=raw.get("description"),
            url=raw["url"],
            platform=ArticlePlatform.DEV_TO,
            reading_time_minutes=raw.get("reading_time_minutes", 0),
            published_at=published_at,
            raw_platform_data=raw,
        )

    async def fetch_data(self, username: str, **kwargs) -> list[ScrapedArticle]:
        api_key = kwargs.get("api_key")
        """
        Fetches the user's articles from Dev.to REST API.

        Args:
            username: Dev.to username.
            api_key: Dev.to API key (optional).

        Returns:
            List of ``ScrapedArticle`` objects.

        Raises:
            DevToScraperError: If API request fails (4xx / 5xx or network error)
                               or if the username is invalid.
         """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise DevToScraperError("Invalid DevTo username format.")

        url = f"{_DEVTO_API_BASE}/articles" f"?username={username}&per_page={_DEFAULT_PER_PAGE}"
        headers = DevToScraperService._build_headers(api_key)

        logger.info("[DEV_TO] Fetching articles for user=%s", username)

        response = await fetch_url(
            url=url,
            headers=headers,
            timeout=_DEFAULT_TIMEOUT,
            error_class=DevToScraperError,
            platform_name="DEV_TO",
        )

        raw_articles: list[dict] = response.json()
        logger.info("[DEV_TO] Received %d articles for user=%s", len(raw_articles), username)

        articles: list[ScrapedArticle] = []
        for raw in raw_articles:
            try:
                articles.append(DevToScraperService._parse_article(raw))
            except Exception as exc:
                # Do not let a single bad article break the entire list
                logger.warning(
                    "[DEV_TO] Skipping article id=%s due to parse error: %s",
                    raw.get("id", "unknown"),
                    exc,
                )

        logger.info("[DEV_TO] Parsed %d articles for user=%s", len(articles), username)
        return articles


# Alias for backward compatibility
DevToScraper = DevToScraperService
