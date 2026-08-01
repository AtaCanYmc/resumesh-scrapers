"""
Substack Provider implementing BaseProvider contract.
"""

from typing import Optional
from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import SubstackScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.substack.mapper import SubstackMapper
from resumesh_scrapers.providers.substack.parser import SubstackParser


class SubstackProvider(BaseProvider):
    """Substack Platform Data Provider."""

    PLATFORM_NAME = "substack"

    async def get_articles(self, identifier: str) -> list[Article]:
        subdomain = identifier.lower().replace(".substack.com", "").lstrip("@")
        cache_key = f"substack:articles:{subdomain}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        url = f"https://{subdomain}.substack.com/feed"
        try:
            response = await self.http_client.get(url)
            parsed_entries = SubstackParser.parse_feed(response.text)
            articles = [SubstackMapper.to_article(e) for e in parsed_entries]
            await self.cache.set(cache_key, articles)
            return articles
        except Exception as e:
            raise SubstackScraperError(f"Failed to fetch Substack feed for {subdomain}: {e}") from e

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        return SubstackMapper.to_profile(identifier)

    async def get_projects(self, identifier: str) -> list[Project]:
        return []
