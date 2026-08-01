"""
Behance Provider implementing BaseProvider contract.
"""

from typing import Optional
from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import BehanceScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.behance.mapper import BehanceMapper
from resumesh_scrapers.providers.behance.parser import BehanceParser


class BehanceProvider(BaseProvider):
    """Behance Platform Data Provider."""

    PLATFORM_NAME = "behance"

    async def get_projects(self, identifier: str) -> list[Project]:
        clean_user = identifier.strip("@")
        cache_key = f"behance:projects:{clean_user}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        api_key = self.credential_provider.get_credential("behance")
        try:
            if api_key:
                url = f"https://api.behance.net/v2/users/{clean_user}/projects?api_key={api_key}"
                response = await self.http_client.get(url)
                data = response.json()
                parsed = BehanceParser.parse_api_projects(data.get("projects", []))
            else:
                url = f"https://www.behance.net/{clean_user}"
                response = await self.http_client.get(url)
                parsed = BehanceParser.parse_html_projects(response.text)

            projects = [BehanceMapper.to_project(p) for p in parsed]
            await self.cache.set(cache_key, projects)
            return projects
        except Exception as e:
            raise BehanceScraperError(f"Failed to fetch Behance projects for {clean_user}: {e}") from e

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        return BehanceMapper.to_profile(identifier)

    async def get_articles(self, identifier: str) -> list[Article]:
        return []
