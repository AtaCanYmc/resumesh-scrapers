"""
GitHub Provider implementing BaseProvider contract.
"""

from typing import Optional

from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import GitHubScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.github.mapper import GitHubMapper
from resumesh_scrapers.providers.github.parser import GitHubParser


class GitHubProvider(BaseProvider):
    """GitHub Platform Data Provider."""

    PLATFORM_NAME = "github"

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        cache_key = f"github:profile:{identifier}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        token = self.credential_provider.get_credential("github")
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = f"https://api.github.com/users/{identifier}"
        try:
            response = await self.http_client.get(url, headers=headers)
            raw = response.json()
            parsed = GitHubParser.parse_user(raw)
            profile = GitHubMapper.to_profile(parsed)
            await self.cache.set(cache_key, profile)
            return profile
        except Exception as e:
            if getattr(e, "status_code", None) == 404:
                return None
            raise GitHubScraperError(f"Failed to fetch GitHub profile for {identifier}: {e}") from e

    async def get_projects(self, identifier: str, include_forks: bool = False) -> list[Project]:
        cache_key = f"github:projects:{identifier}:{include_forks}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        token = self.credential_provider.get_credential("github")
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = f"https://api.github.com/users/{identifier}/repos?per_page=100&sort=updated"
        try:
            response = await self.http_client.get(url, headers=headers)
            raw_repos = response.json()
            projects = []
            for raw in raw_repos:
                if not include_forks and raw.get("fork"):
                    continue
                parsed = GitHubParser.parse_repo(raw)
                projects.append(GitHubMapper.to_project(parsed))

            await self.cache.set(cache_key, projects)
            return projects
        except Exception as e:
            raise GitHubScraperError(f"Failed to fetch GitHub repositories for {identifier}: {e}") from e

    async def get_articles(self, identifier: str) -> list[Article]:
        return []
