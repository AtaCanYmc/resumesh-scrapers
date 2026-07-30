"""
PyPI Scraper Service
====================
Fetches package details using the official PyPI JSON API
and returns them as ``ScrapedProject`` models.

Usage:
    from resumesh_scrapers import PyPIScraperService

    scraper = PyPIScraperService()
    # PyPI requires specific package names (e.g., ['resumesh-scrapers', 'logport'])
    packages = await scraper.fetch_data(username="atacanymc", package_names=["resumesh-scrapers"])

API Reference:
    GET https://pypi.org/pypi/{package_name}/json
"""

import logging
import re
from typing import List

from bs4 import BeautifulSoup

from resumesh_scrapers.core.client import fetch_url
from resumesh_scrapers.exceptions import PyPIScraperError
from resumesh_scrapers.models import PyPiPackageModel
from resumesh_scrapers.platforms.base import IScraperService

logger = logging.getLogger(__name__)

_PYPI_API_BASE = "https://pypi.org/pypi/{package_name}/json"
_PYPI_API_PACKAGES = "https://pypi.org/user/{username}/"
_DEFAULT_TIMEOUT = 15.0


class PyPIScraperService(IScraperService):
    """
    Service that fetches package metadata using the PyPI JSON API.
    """

    @staticmethod
    async def fetch_package_names(username: str):
        """
        Fetches package names from PyPI.
        """
        url = _PYPI_API_PACKAGES.format(username=username)

        response = await fetch_url(url=url, timeout=_DEFAULT_TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")

        packages = [h3.text.strip() for h3 in soup.find_all("h3", class_="package-snippet__title")]

        return packages

    async def fetch_data(self, username: str, **kwargs) -> List[PyPiPackageModel]:
        """
        Fetches package metadata from PyPI.

        Args:
            username: PyPI author/maintainer username (used for logging/filtering).
            **kwargs: Can include `package_names` (list[str]) specifying which packages to fetch.

        Returns:
            List of ``PyPiPackageModel`` objects.

        Raises:
            PyPIScraperError: If API request fails.
        """
        package_names = kwargs.get("package_names", [])
        if not package_names or len(package_names) == 0:
            package_names = await self.fetch_package_names(username=username)

        projects: List[PyPiPackageModel] = []
        for pkg_name in package_names:
            if not re.match(r"^[a-zA-Z0-9\-_]+$", pkg_name):
                logger.warning("[PYPI] Skipping invalid package name format: %s", pkg_name)
                continue

            url = _PYPI_API_BASE.format(package_name=pkg_name)
            logger.info("[PYPI] Fetching package metadata for package=%s", pkg_name)

            try:
                response = await fetch_url(
                    url=url,
                    timeout=_DEFAULT_TIMEOUT,
                    follow_redirects=True,
                    error_class=PyPIScraperError,
                    platform_name="PYPI",
                )
                data = response.json()
                projects.append(PyPiPackageModel.model_validate(data))
            except Exception as exc:
                logger.warning("[PYPI] Failed to fetch package '%s': %s", pkg_name, exc)

        logger.info(
            "[PYPI] Successfully parsed %d packages for user=%s",
            len(projects),
            username,
        )
        return projects


# Alias for backward compatibility
PyPIScraper = PyPIScraperService
