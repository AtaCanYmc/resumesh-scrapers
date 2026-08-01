"""
Medium Provider implementing BaseProvider contract.
"""

from typing import Optional

from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import MediumScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.medium.mapper import MediumMapper
from resumesh_scrapers.providers.medium.parser import MediumParser


class MediumProvider(BaseProvider):
    """Medium Platform Data Provider."""

    PLATFORM_NAME = "medium"

    async def get_articles(self, identifier: str) -> list[Article]:
        clean_username = identifier.lstrip("@")
        cache_key = f"medium:articles:{clean_username}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        url = f"https://medium.com/feed/@{clean_username}"
        try:
            response = await self.http_client.get(url)
            parsed_entries = MediumParser.parse_feed(response.text)
            articles = [MediumMapper.to_article(e) for e in parsed_entries]
            await self.cache.set(cache_key, articles)
            return articles
        except Exception as e:
            raise MediumScraperError(f"Failed to fetch Medium feed for @{clean_username}: {e}") from e

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        return MediumMapper.to_profile(identifier)

    async def get_projects(self, identifier: str) -> list[Project]:
        return []
