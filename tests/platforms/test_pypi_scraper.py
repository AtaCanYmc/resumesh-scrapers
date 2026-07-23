"""Tests for PyPIScraperService."""

import httpx
import pytest
import respx
from httpx import Response
from resumesh_scrapers.models import PyPiPackageModel
from resumesh_scrapers.platforms import PyPIScraperService

# Mock data simulating official PyPI JSON API response
SAMPLE_PYPI_RESPONSE = {
    "info": {
        "name": "resumesh-scrapers",
        "version": "0.1.0",
        "summary": "Standalone web scraping services",
        "home_page": "https://github.com/AtaCanYmc/resumesh-scrapers",
        "author": "Ata Can Yaymacı",
        "downloads": {"last_day": 10, "last_week": 50, "last_month": 200},
    },
    "last_serial": 123456,
    "ownership": {"roles": [{"role": "Owner", "user": "atacanymc"}]},
    "releases": {
        "0.1.0": [
            {
                "filename": "resumesh_scrapers-0.1.0-py3-none-any.whl",
                "size": 1024,
                "upload_time": "2024-07-14T12:00:00",
                "upload_time_iso_8601": "2024-07-14T12:00:00Z",
                "url": "https://files.pythonhosted.org/.../resumesh_scrapers-0.1.0-py3-none-any.whl",
                "digests": {"blake2b_256": "abc", "md5": "def", "sha256": "ghi"},
                "downloads": 100,
                "has_sig": False,
                "md5_digest": "def",
                "packagetype": "bdist_wheel",
                "python_version": "py3",
                "yanked": False,
            }
        ]
    },
    "urls": [],
    "vulnerabilities": [],
}


@pytest.fixture
def scraper():
    return PyPIScraperService()


class TestPyPIScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_package_success(self, scraper):
        respx.get("https://pypi.org/pypi/resumesh-scrapers/json").mock(
            return_value=Response(200, json=SAMPLE_PYPI_RESPONSE)
        )
        packages = await scraper.fetch_data("atacanymc", package_names=["resumesh-scrapers"])
        assert len(packages) == 1
        assert all(isinstance(p, PyPiPackageModel) for p in packages)
        assert packages[0].info.name == "resumesh-scrapers"
        assert packages[0].info.version == "0.1.0"

    @pytest.mark.asyncio
    async def test_fetch_packages_empty_names(self, scraper):
        packages = await scraper.fetch_data("atacanymc", package_names=[])
        assert packages == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_package_http_error(self, scraper):
        respx.get("https://pypi.org/pypi/unknown-pkg/json").mock(return_value=Response(404, text="Not Found"))
        # Should catch the error gracefully and log warning instead of crashing batch
        packages = await scraper.fetch_data("atacanymc", package_names=["unknown-pkg"])
        assert packages == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_package_network_error(self, scraper):
        respx.get("https://pypi.org/pypi/resumesh-scrapers/json").mock(side_effect=httpx.ConnectError("timeout"))
        packages = await scraper.fetch_data("atacanymc", package_names=["resumesh-scrapers"])
        assert packages == []
