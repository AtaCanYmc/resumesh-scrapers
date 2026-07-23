"""
Substack Scraper Service
========================
Fetches the publication's articles using Substack's public RSS feed URL
and returns them as ``ScrapedArticle`` models.

Usage:
    from resumesh_scrapers import SubstackScraperService

    scraper = SubstackScraperService()
    articles = await scraper.fetch_data(publication="atacan")

Feed URL Format:
    https://{publication}.substack.com/feed
"""

import html
import logging
import re
from datetime import datetime, timezone

import feedparser

from resumesh_scrapers.platforms.base import IScraperService
from resumesh_scrapers.core.client import fetch_url
from resumesh_scrapers.exceptions import SubstackScraperError
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle

logger = logging.getLogger(__name__)

_SUBSTACK_FEED_BASE = "https://{publication}.substack.com/feed"
_DEFAULT_TIMEOUT = 20.0


class SubstackScraperService(IScraperService):
    """
    Service that fetches and parses Substack RSS feed.
    """

    def _parse_entry(entry: feedparser.FeedParserDict) -> ScrapedArticle:
        """
        Converts a single RSS entry from feedparser to ``ScrapedArticle``.

        Args:
            entry: RSS entry parsed by feedparser.

        Returns:
            A ``ScrapedArticle`` object.
        """
        # Clean UTM and tracking parameters from URL if present
        clean_url = entry.link.split("?")[0] if entry.get("link") else ""

        # Convert publish date to UTC datetime
        if entry.get("published_parsed"):
            published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        else:
            published_at = datetime.now(timezone.utc)
            logger.debug(
                "[SUBSTACK] No published_parsed for entry='%s', using now()",
                entry.get("title", "unknown"),
            )

        tags = [t.term for t in entry.tags] if entry.get("tags") else []

        raw_summary = entry.get("summary", "") or ""
        clean_summary = re.sub(r"<[^>]+>", "", raw_summary).strip()
        clean_summary = html.unescape(clean_summary)

        # Estimate reading time based on summary/content length (approx 200 words per minute)
        word_count = len(clean_summary.split())
        reading_time = max(1, word_count // 200)

        return ScrapedArticle(
            title=entry.get("title", "Untitled"),
            summary=clean_summary[:300] if clean_summary else None,
            url=clean_url,
            platform=ArticlePlatform.SUBSTACK,
            reading_time_minutes=reading_time,
            published_at=published_at,
            raw_platform_data={"tags": tags},
        )

    async def fetch_data(self, publication: str, **kwargs) -> list[ScrapedArticle]:
        """
        Fetches the publication's articles from Substack RSS feed.

        Args:
            publication: Substack publication subdomain or identifier (e.g., 'atacan' for atacan.substack.com).

        Returns:
            List of ``ScrapedArticle`` objects.

        Raises:
            SubstackScraperError: If RSS feed cannot be fetched,
                                  HTTP error occurs, or the publication name is invalid.
        """
        # Clean potential "@" or full urls if passed by mistake
        clean_pub = publication.strip("@").split(".")[0]

        if not re.match(r"^[a-zA-Z0-9\-]+$", clean_pub):
            raise SubstackScraperError("Invalid Substack publication format.")

        url = _SUBSTACK_FEED_BASE.format(publication=clean_pub)
        logger.info("[SUBSTACK] Fetching RSS feed for publication=%s", clean_pub)

        response = await fetch_url(
            url=url,
            timeout=_DEFAULT_TIMEOUT,
            follow_redirects=True,
            error_class=SubstackScraperError,
            platform_name="SUBSTACK",
        )

        feed = feedparser.parse(response.text)

        if feed.bozo:
            logger.warning(
                "[SUBSTACK] RSS parse warning for publication=%s: %s",
                clean_pub,
                feed.bozo_exception,
            )

        logger.info(
            "[SUBSTACK] Received %d entries from RSS for publication=%s",
            len(feed.entries),
            clean_pub,
        )

        articles: list[ScrapedArticle] = []
        for entry in feed.entries:
            try:
                articles.append(SubstackScraperService._parse_entry(entry))
            except Exception as exc:
                logger.warning(
                    "[SUBSTACK] Skipping entry title='%s' due to parse error: %s",
                    entry.get("title", "unknown"),
                    exc,
                )

        logger.info("[SUBSTACK] Parsed %d articles for publication=%s", len(articles), clean_pub)
        return articles


# Alias for backward compatibility
SubstackScraper = SubstackScraperService
