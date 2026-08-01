"""
PyPI Provider implementing BaseProvider contract.
"""

from typing import Optional

from resumesh_scrapers.domain import Article, Profile, Project
from resumesh_scrapers.exceptions import PyPIScraperError
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.pypi.mapper import PyPiMapper
from resumesh_scrapers.providers.pypi.parser import PyPiParser


class PyPiProvider(BaseProvider):
    """PyPI Package Registry Platform Data Provider."""

    PLATFORM_NAME = "pypi"

    async def get_projects(self, identifier: str, package_names: Optional[list[str]] = None) -> list[Project]:
        clean_user = identifier.strip("@")
        cache_key = f"pypi:projects:{clean_user}:{package_names}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            if not package_names:
                profile_url = f"https://pypi.org/user/{clean_user}/"
                res = await self.http_client.get(profile_url)
                package_names = PyPiParser.parse_profile_packages(res.text)

            projects = []
            for pkg_name in package_names:
                url = f"https://pypi.org/pypi/{pkg_name}/json"
                try:
                    res = await self.http_client.get(url)
                    parsed = PyPiParser.parse_package(res.json())
                    projects.append(PyPiMapper.to_project(parsed))
                except Exception:
                    pass

            await self.cache.set(cache_key, projects)
            return projects
        except Exception as e:
            raise PyPIScraperError(f"Failed to fetch PyPI packages for {clean_user}: {e}") from e

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        return PyPiMapper.to_profile(identifier)

    async def get_articles(self, identifier: str) -> list[Article]:
        return []
