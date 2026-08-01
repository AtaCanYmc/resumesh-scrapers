"""
Dev.to Provider implementing BaseProvider contract.
"""

from typing import Optional
from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import DevToScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.devto.mapper import DevToMapper
from resumesh_scrapers.providers.devto.parser import DevToParser


class DevToProvider(BaseProvider):
    """Dev.to Platform Data Provider."""

    PLATFORM_NAME = "devto"

    async def get_articles(self, identifier: str) -> list[Article]:
        cache_key = f"devto:articles:{identifier}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        api_key = self.credential_provider.get_credential("devto")
        headers = {"Accept": "application/vnd.forem.api-v1+json"}
        if api_key:
            headers["api-key"] = api_key

        url = f"https://dev.to/api/articles?username={identifier}&per_page=1000"
        try:
            response = await self.http_client.get(url, headers=headers)
            raw_articles = response.json()
            articles = []
            for raw in raw_articles:
                parsed = DevToParser.parse_article(raw)
                articles.append(DevToMapper.to_article(parsed))

            await self.cache.set(cache_key, articles)
            return articles
        except Exception as e:
            raise DevToScraperError(f"Failed to fetch Dev.to articles for {identifier}: {e}") from e

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        articles = await self.get_articles(identifier)
        if not articles:
            return Profile(platform="devto", username=identifier, website=f"https://dev.to/{identifier}")
        first_raw = articles[0].raw_extra.get("user", {})
        parsed = DevToParser.parse_article({"user": first_raw})
        return DevToMapper.to_profile(parsed["user"])

    async def get_projects(self, identifier: str) -> list[Project]:
        return []
