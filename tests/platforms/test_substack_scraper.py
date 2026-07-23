"""Tests for SubstackScraperService."""

import httpx
import pytest
import respx
from httpx import Response
from resumesh_scrapers.exceptions import SubstackScraperError
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle
from resumesh_scrapers.platforms.substack import SubstackScraperService

SAMPLE_SUBSTACK_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Substack Feed</title>
    <link>https://atacan.substack.com</link>
    <item>
      <title>My Substack Article</title>
      <link>https://atacan.substack.com/p/my-substack-article?utm_source=substack</link>
      <pubDate>Mon, 01 Jul 2024 12:00:00 GMT</pubDate>
      <description><![CDATA[<p>This is a <b>substack</b> post with some words to calculate reading time.</p>]]></description>
      <category>tech</category>
    </item>
    <item>
      <title>Untitled Post</title>
      <link>https://atacan.substack.com/p/untitled</link>
      <pubDate>Wed, 10 Jul 2024 08:00:00 GMT</pubDate>
      <description>Short summary</description>
    </item>
  </channel>
</rss>
"""


@pytest.fixture
def scraper():
    return SubstackScraperService()


class TestSubstackScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_success(self, scraper):
        respx.get("https://atacan.substack.com/feed").mock(return_value=Response(200, text=SAMPLE_SUBSTACK_FEED))

        articles = await scraper.fetch_data("atacan")

        assert len(articles) == 2
        assert all(isinstance(a, ScrapedArticle) for a in articles)
        assert articles[0].title == "My Substack Article"
        assert articles[0].platform == ArticlePlatform.SUBSTACK
        assert articles[0].reading_time_minutes == 1  # 10 words / 200 = 0 -> min 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_http_error(self, scraper):
        respx.get("https://atacan.substack.com/feed").mock(return_value=Response(404, text="Not Found"))

        with pytest.raises(SubstackScraperError) as exc_info:
            await scraper.fetch_data("@atacan")  # testing strip '@' as well
        assert exc_info.value.status_code == 404

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_articles_network_error(self, scraper):
        respx.get("https://atacan.substack.com/feed").mock(side_effect=httpx.ConnectError("dns lookup failure"))

        with pytest.raises(SubstackScraperError, match="Network error"):
            await scraper.fetch_data("atacan")

    @pytest.mark.asyncio
    async def test_invalid_publication_format(self, scraper):
        with pytest.raises(SubstackScraperError, match="Invalid Substack publication"):
            await scraper.fetch_data("invalid pub!")
