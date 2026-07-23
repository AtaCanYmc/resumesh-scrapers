"""Tests for NpmScraperService."""

import httpx
import pytest
import respx
from httpx import Response

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms import NpmScraperService
from resumesh_scrapers.models import NpmSearchResultModel

# Mock data simulating npm registry search response
SAMPLE_NPM_RESPONSE = {
    "objects": [
        {
            "package": {
                "name": "resumesh-scrapers",
                "description": "Standalone web scraping services",
                "version": "0.1.0",
                "keywords": ["scraper", "python"],
                "links": {
                    "npm": "https://www.npmjs.com/package/resumesh-scrapers",
                    "repository": "https://github.com/AtaCanYmc/resumesh-scrapers"
                },
                "publisher": {
                    "username": "atacanymc"
                }
            },
            "score": {
                "final": 0.95
            }
        }
    ],
    "total": 1
}


@pytest.fixture
def scraper():
    return NpmScraperService()


class TestNpmScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_packages_success(self, scraper):
        respx.get("https://registry.npmjs.org/-/v1/search").mock(
            return_value=Response(200, json=SAMPLE_NPM_RESPONSE)
        )
        packages = await scraper.fetch_data("atacanymc")
        assert len(packages) == 1
        assert all(isinstance(p, NpmSearchResultModel) for p in packages)
        assert packages[0].objects[0].package.name == "resumesh-scrapers"

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_packages_empty(self, scraper):
        respx.get("https://registry.npmjs.org/-/v1/search").mock(
            return_value=Response(200, json={"objects": [], "total": 0})
        )
        packages = await scraper.fetch_data("atacanymc")
        assert packages == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_packages_http_error(self, scraper):
        respx.get("https://registry.npmjs.org/-/v1/search").mock(
            return_value=Response(500, text="Registry Error")
        )
        with pytest.raises(ScraperError) as exc_info:
            await scraper.fetch_data("atacanymc")
        assert exc_info.value.status_code == 500

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_packages_network_error(self, scraper):
        respx.get("https://registry.npmjs.org/-/v1/search").mock(
            side_effect=httpx.ConnectError("connection timeout")
        )
        with pytest.raises(ScraperError, match="Network error"):
            await scraper.fetch_data("atacanymc")

    @pytest.mark.asyncio
    async def test_invalid_username(self, scraper):
        with pytest.raises(ScraperError, match="Invalid npm username"):
            await scraper.fetch_data("invalid user name!")
