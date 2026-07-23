import asyncio
import logging

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.devto import DevToScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "atacanymc"
    try:
        logger.info(f"Fetching Dev.to articles for: {username}")
        devto_scraper = DevToScraper()
        devto_data = await devto_scraper.fetch_data(username)
        logger.info(f"Dev.to success: {len(devto_data)} articles found.")
        for article in devto_data[:3]:
            logger.info(f"- {article.title} ({article.reading_time_minutes} min read)")
    except ScraperError as e:
        logger.error(f"Dev.to scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
