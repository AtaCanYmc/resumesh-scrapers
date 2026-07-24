"""Tests for DevToScraperService."""
from typing import List

import httpx
import pytest
import respx
from httpx import Response
from resumesh_scrapers.exceptions import DevToScraperError
from resumesh_scrapers.models import DevToArticleModel
from resumesh_scrapers.platforms import DevToScraperService

# ── Fixtures ────────────────────────────────────────────────────────────────

SAMPLE_ARTICLES: List[DevToArticleModel] = [
    {
        "id": 1001,
        "title": "Getting Started with FastAPI",
        "description": "A beginner's guide to FastAPI",
        "url": "https://dev.to/atacanymc/getting-started-with-fastapi-1a2b",
        "published_at": "2024-06-15T10:30:00Z",
        "reading_time_minutes": 7,
    },
    {
        "id": 1002,
        "title": "Advanced Python Patterns",
        "description": "Exploring design patterns in Python",
        "url": "https://dev.to/atacanymc/advanced-python-patterns-3c4d",
        "published_at": "2024-07-01T08:00:00Z",
        "reading_time_minutes": 12,
    },
]


@pytest.fixture
def scraper():
    return DevToScraperService()


# ── Tests ───────────────────────────────────────────────────────────────────


class TestDevToScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_success(self, scraper):
        respx.get("https://dev.to/api/articles").mock(return_value=Response(200, json=SAMPLE_ARTICLES))

        articles = await scraper.fetch_data("atacanymc")

        assert len(articles) == 2
        assert all(isinstance(a, DevToArticleModel) for a in articles)
        assert articles[0].title == "Getting Started with FastAPI"
        assert articles[0].reading_time_minutes == 7

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_empty(self, scraper):
        respx.get("https://dev.to/api/articles").mock(return_value=Response(200, json=[]))

        articles = await scraper.fetch_data("atacanymc")
        assert articles == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_http_error(self, scraper):
        respx.get("https://dev.to/api/articles").mock(return_value=Response(500, text="Internal Server Error"))

        with pytest.raises(DevToScraperError) as exc_info:
            await scraper.fetch_data("atacanymc")

        assert exc_info.value.status_code == 500

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_network_error(self, scraper):
        respx.get("https://dev.to/api/articles").mock(side_effect=httpx.ConnectError("timeout"))

        with pytest.raises(DevToScraperError, match="Network error"):
            await scraper.fetch_data("atacanymc")

    @pytest.mark.asyncio
    async def test_invalid_username(self, scraper):
        with pytest.raises(DevToScraperError, match="Invalid DevTo username"):
            await scraper.fetch_data("bad user name!")

    @respx.mock
    @pytest.mark.asyncio
    async def test_skips_unparseable_article(self, scraper):
        """A single malformed article should not break the entire batch."""
        bad_articles = [
            {"id": 999},  # missing required 'title' and 'url'
            SAMPLE_ARTICLES[0],
        ]
        respx.get("https://dev.to/api/articles").mock(return_value=Response(200, json=bad_articles))

        articles = await scraper.fetch_data("atacanymc")
        assert len(articles) == 1
        assert articles[0].title == "Getting Started with FastAPI"


class TestDevToScraperHeaders:
    def test_headers_without_api_key(self):
        headers = DevToScraperService._build_headers()
        assert "Accept" in headers
        assert "api-key" not in headers

    def test_headers_with_api_key(self):
        headers = DevToScraperService._build_headers(api_key="test_key_123")
        assert headers["api-key"] == "test_key_123"
