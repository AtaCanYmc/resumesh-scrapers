"""Tests for MediumScraperService."""

import httpx
import pytest
import respx
from httpx import Response

from resumesh_scrapers.exceptions import MediumScraperError
from resumesh_scrapers.platforms import MediumScraperService
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle

# ── Fixtures ────────────────────────────────────────────────────────────────

SAMPLE_RSS_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Medium Feed</title>
    <link>https://medium.com/@testuser</link>
    <item>
      <title>My First Post</title>
      <link>https://medium.com/@testuser/my-first-post-abc123?source=rss</link>
      <pubDate>Sat, 15 Jun 2024 12:00:00 GMT</pubDate>
      <description><![CDATA[<p>This is a <b>great</b> article about &amp; stuff.</p>]]></description>
      <category>python</category>
      <category>tutorial</category>
    </item>
    <item>
      <title>My Second Post</title>
      <link>https://medium.com/@testuser/my-second-post-def456</link>
      <pubDate>Mon, 01 Jul 2024 08:00:00 GMT</pubDate>
      <description>Simple summary without HTML</description>
    </item>
  </channel>
</rss>
"""

EMPTY_RSS_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Empty Feed</title>
    <link>https://medium.com/@nobody</link>
  </channel>
</rss>
"""


@pytest.fixture
def scraper():
    return MediumScraperService()


# ── Tests ───────────────────────────────────────────────────────────────────


class TestMediumScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_success(self, scraper):
        respx.get("https://medium.com/feed/@testuser").mock(
            return_value=Response(200, text=SAMPLE_RSS_FEED)
        )

        articles = await scraper.fetch_data("testuser")

        assert len(articles) == 2
        assert all(isinstance(a, ScrapedArticle) for a in articles)
        assert articles[0].title == "My First Post"
        assert articles[0].platform == ArticlePlatform.MEDIUM

    @respx.mock
    @pytest.mark.asyncio
    async def test_url_tracking_params_stripped(self, scraper):
        respx.get("https://medium.com/feed/@testuser").mock(
            return_value=Response(200, text=SAMPLE_RSS_FEED)
        )

        articles = await scraper.fetch_data("testuser")

        url_str = str(articles[0].url)
        assert "?source=rss" not in url_str
        assert url_str.endswith("abc123")

    @respx.mock
    @pytest.mark.asyncio
    async def test_html_stripped_from_summary(self, scraper):
        respx.get("https://medium.com/feed/@testuser").mock(
            return_value=Response(200, text=SAMPLE_RSS_FEED)
        )

        articles = await scraper.fetch_data("testuser")

        # HTML tags should be stripped, entities unescaped
        assert "<p>" not in articles[0].summary
        assert "<b>" not in articles[0].summary
        assert "& stuff" in articles[0].summary

    @respx.mock
    @pytest.mark.asyncio
    async def test_tags_extracted(self, scraper):
        respx.get("https://medium.com/feed/@testuser").mock(
            return_value=Response(200, text=SAMPLE_RSS_FEED)
        )

        articles = await scraper.fetch_data("testuser")

        assert articles[0].raw_platform_data["tags"] == ["python", "tutorial"]

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_empty_feed(self, scraper):
        respx.get("https://medium.com/feed/@nobody").mock(
            return_value=Response(200, text=EMPTY_RSS_FEED)
        )

        articles = await scraper.fetch_data("nobody")
        assert articles == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_http_error(self, scraper):
        respx.get("https://medium.com/feed/@testuser").mock(
            return_value=Response(404, text="Not Found")
        )

        with pytest.raises(MediumScraperError) as exc_info:
            await scraper.fetch_data("testuser")

        assert exc_info.value.status_code == 404

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_network_error(self, scraper):
        respx.get("https://medium.com/feed/@testuser").mock(
            side_effect=httpx.ConnectError("dns failure")
        )

        with pytest.raises(MediumScraperError, match="Network error"):
            await scraper.fetch_data("testuser")

    @pytest.mark.asyncio
    async def test_invalid_username(self, scraper):
        with pytest.raises(MediumScraperError, match="Invalid Medium username"):
            await scraper.fetch_data("bad user!")

    @respx.mock
    @pytest.mark.asyncio
    async def test_reading_time_always_zero(self, scraper):
        """Medium RSS doesn't provide reading time — should always be 0."""
        respx.get("https://medium.com/feed/@testuser").mock(
            return_value=Response(200, text=SAMPLE_RSS_FEED)
        )

        articles = await scraper.fetch_data("testuser")
        for article in articles:
            assert article.reading_time_minutes == 0
