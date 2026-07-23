"""Tests for BehanceScraperService."""

import httpx
import pytest
import respx
from httpx import Response

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.behance import (
    BehanceScraperService,
    BehanceScraperError,
)
from resumesh_scrapers.models import BehanceProjectModel

SAMPLE_BEHANCE_HTML = """
<html>
<body>
    <div class="project-card">
        <a class="projekt-link" href="/gallery/12345/My-Awesome-Design">My Awesome Design</a>
        <a href="/gallery/12345/My-Awesome-Design">View</a>
        <div class="Stat--appreciations">150</div>
    </div>
    <div class="ProjectCover-wrapper">
        <a class="ProjectCover-title" href="/gallery/67890/Second-Art">Second Art</a>
        <a href="/gallery/67890/Second-Art">View</a>
        <span class="ProjectCover-appreciations">Appreciations: 42</span>
    </div>
    <div class="project-card">
        <!-- Broken card with no link -->
        <h3>No Link Project</h3>
    </div>
</body>
</html>
"""


@pytest.fixture
def scraper():
    return BehanceScraperService()


class TestBehanceScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_projects_success(self, scraper):
        respx.get("https://www.behance.net/testuser").mock(
            return_value=Response(200, text=SAMPLE_BEHANCE_HTML)
        )

        projects = await scraper.fetch_data("testuser")

        assert len(projects) == 2
        assert all(isinstance(p, BehanceProjectModel) for p in projects)
        assert projects[0].name == "My Awesome Design"
        assert (
            str(projects[0].url)
            == "https://www.behance.net/gallery/12345/My-Awesome-Design"
        )
        assert projects[0].stats_appreciations == 150
        assert projects[1].name == "Second Art"
        assert projects[1].stats_appreciations == 42

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_projects_http_error(self, scraper):
        respx.get("https://www.behance.net/testuser").mock(
            return_value=Response(404, text="Not Found")
        )

        with pytest.raises(BehanceScraperError) as exc_info:
            await scraper.fetch_data("@testuser")  # testing strip '@' as well
        assert exc_info.value.status_code == 404

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_projects_network_error(self, scraper):
        respx.get("https://www.behance.net/testuser").mock(
            side_effect=httpx.ConnectError("connection timed out")
        )

        with pytest.raises(BehanceScraperError, match="Network error"):
            await scraper.fetch_data("testuser")

    @pytest.mark.asyncio
    async def test_invalid_username(self, scraper):
        with pytest.raises(BehanceScraperError, match="Invalid Behance username"):
            await scraper.fetch_data("invalid user!")
