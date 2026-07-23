"""
NPM Scraper Service
=====================
Fetches the user's published packages using the public npm registry API
and returns them as ``NpmSearchResultModel`` models.

Usage:
    from resumesh_scrapers import NpmScraperService

    scraper = NpmScraperService()
    packages = await scraper.fetch_data(username="atacanymc")

API Reference:
    GET https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=100&from=0
"""

import logging
import re
from typing import List

from resumesh_scrapers.exceptions import NpmScraperError
from resumesh_scrapers.models import NpmSearchResultModel
from resumesh_scrapers.platforms.base import IScraperService
from resumesh_scrapers.core.client import fetch_url

logger = logging.getLogger(__name__)

_NPM_SEARCH_URL = "https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=100&from=0"
_DEFAULT_TIMEOUT = 15.0


class NpmScraperService(IScraperService):
    """
    Service that fetches package data using the public npm registry API.
    """

    async def fetch_data(self, username: str, **kwargs) -> List[NpmSearchResultModel]:
        """
        Fetches the user's published packages from the npm registry.

        Args:
            username: npm maintainer username.

        Returns:
            List of ``NpmSearchResultModel`` objects.

        Raises:
            NpmScraperError: If the API request fails or format is invalid.
        """
        clean_user = username.strip("@")
        if not re.match(r"^[a-zA-Z0-9\-_]+$", clean_user):
            raise NpmScraperError("Invalid npm username format.")

        url = _NPM_SEARCH_URL.format(username=clean_user)
        logger.info("[NPM] Fetching packages for maintainer=%s", clean_user)

        response = await fetch_url(
            url=url,
            timeout=_DEFAULT_TIMEOUT,
            follow_redirects=True,
            error_class=NpmScraperError,
            platform_name="NPM",
        )

        try:
            data = response.json()
        except Exception as exc:
            raise NpmScraperError(f"Failed to parse JSON response from npm registry: {exc}")

        logger.info("[NPM] Received response from npm search for maintainer=%s", clean_user)

        try:
            result_model = NpmSearchResultModel.model_validate(data)
            if not result_model.objects:
                return []
            return [result_model]
        except Exception as exc:
            logger.warning("[NPM] Failed to validate NpmSearchResultModel: %s", exc)
            raise NpmScraperError(f"Failed to validate npm search result: {exc}")


# Alias for backward compatibility
NpmScraper = NpmScraperService
