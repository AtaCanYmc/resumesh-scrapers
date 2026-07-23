"""
Medium Scraper Service
========================
Fetches the user's articles using Medium's public RSS feed URL
and returns them as ``ScrapedArticle`` models.

Usage:
    from resumesh_scrapers import MediumScraperService

    scraper = MediumScraperService()
    articles = await scraper.fetch_data(username="atacanymc")

Feed URL Format:
    https://medium.com/feed/@{username}

Note:
    Medium RSS feed does not require an API key. It is parsed using feedparser.
    Medium might embed HTML in RSS contents; summary field could contain raw HTML.
"""

import html
import logging
import re
from datetime import datetime, timezone

import feedparser

from resumesh_scrapers.platforms.base import IScraperService
from resumesh_scrapers.core.client import fetch_url
from resumesh_scrapers.exceptions import MediumScraperError
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle

logger = logging.getLogger(__name__)

_MEDIUM_FEED_BASE = "https://medium.com/feed/@{username}"
_DEFAULT_TIMEOUT = 20.0


class MediumScraperService(IScraperService):
    """
    Service that fetches and parses Medium RSS feed.
    """

    def _parse_entry(entry: feedparser.FeedParserDict) -> ScrapedArticle:
        """
        Converts a single RSS entry from feedparser to ``ScrapedArticle``.

        Args:
            entry: RSS entry parsed by feedparser.

        Returns:
            A ``ScrapedArticle`` object.
        """
        # Clean UTM and tracking parameters from URL
        clean_url = entry.link.split("?")[0]

        # Convert publish date to UTC datetime
        if entry.get("published_parsed"):
            published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        else:
            published_at = datetime.now(timezone.utc)
            logger.debug(
                "[MEDIUM] No published_parsed for entry='%s', using now()",
                entry.get("title", "unknown"),
            )

        tags = [t.term for t in entry.tags] if entry.get("tags") else []

        raw_summary = entry.get("summary", "") or ""
        clean_summary = re.sub(r"<[^>]+>", "", raw_summary).strip()
        clean_summary = html.unescape(clean_summary)

        return ScrapedArticle(
            title=entry.title,
            summary=clean_summary,
            url=clean_url,
            platform=ArticlePlatform.MEDIUM,
            reading_time_minutes=0,  # Medium RSS does not provide this info
            published_at=published_at,
            raw_platform_data={"tags": tags},
        )

    async def fetch_data(self, username: str, **kwargs) -> list[ScrapedArticle]:
        """
        Fetches the user's articles from Medium RSS feed.

        Args:
            username: Medium username (without @ symbol).

        Returns:
            List of ``ScrapedArticle`` objects.

        Raises:
            MediumScraperError: If RSS feed cannot be fetched,
                                HTTP error occurs, or the username is invalid.
        """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise MediumScraperError("Invalid Medium username format.")

        url = _MEDIUM_FEED_BASE.format(username=username)
        logger.info("[MEDIUM] Fetching RSS feed for user=%s", username)

        response = await fetch_url(
            url=url,
            timeout=_DEFAULT_TIMEOUT,
            follow_redirects=True,
            error_class=MediumScraperError,
            platform_name="MEDIUM",
        )

        feed = feedparser.parse(response.text)

        # bozo=True → feedparser warned about ill-formed XML
        # Continue if possible, just log it
        if feed.bozo:
            logger.warning(
                "[MEDIUM] RSS parse warning for user=%s: %s",
                username,
                feed.bozo_exception,
            )

        logger.info(
            "[MEDIUM] Received %d entries from RSS for user=%s",
            len(feed.entries),
            username,
        )

        articles: list[ScrapedArticle] = []
        for entry in feed.entries:
            try:
                articles.append(MediumScraperService._parse_entry(entry))
            except Exception as exc:
                # Do not let a single bad entry break the entire list
                logger.warning(
                    "[MEDIUM] Skipping entry title='%s' due to parse error: %s",
                    entry.get("title", "unknown"),
                    exc,
                )

        logger.info("[MEDIUM] Parsed %d articles for user=%s", len(articles), username)
        return articles


# Alias for backward compatibility
MediumScraper = MediumScraperService
