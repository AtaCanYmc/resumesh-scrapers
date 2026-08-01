"""
NPM Provider implementing BaseProvider contract.
"""

from typing import Optional
from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import NpmScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.npm.mapper import NpmMapper
from resumesh_scrapers.providers.npm.parser import NpmParser


class NpmProvider(BaseProvider):
    """NPM Registry Platform Data Provider."""

    PLATFORM_NAME = "npm"

    async def get_projects(self, identifier: str) -> list[Project]:
        clean_user = identifier.strip("@")
        cache_key = f"npm:projects:{clean_user}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        url = f"https://registry.npmjs.org/-/v1/search?text=maintainer:{clean_user}&size=100&from=0"
        try:
            response = await self.http_client.get(url)
            data = response.json()
            parsed_pkgs = NpmParser.parse_objects(data)
            projects = [NpmMapper.to_project(p) for p in parsed_pkgs]
            await self.cache.set(cache_key, projects)
            return projects
        except Exception as e:
            raise NpmScraperError(f"Failed to fetch npm packages for {clean_user}: {e}") from e

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        return NpmMapper.to_profile(identifier)

    async def get_articles(self, identifier: str) -> list[Article]:
        return []
