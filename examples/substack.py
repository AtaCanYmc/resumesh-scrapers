import asyncio
import logging

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.substack import SubstackScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    publication = "atacan"
    try:
        logger.info(f"Fetching Substack articles for publication: {publication}")
        substack_scraper = SubstackScraper()
        substack_data = await substack_scraper.fetch_data(publication)
        logger.info(f"Substack success: {len(substack_data)} articles found.")
        for article in substack_data[:3]:
            logger.info(f"- {article.title} ({article.reading_time_minutes} min read)")
    except ScraperError as e:
        logger.error(f"Substack scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
