import asyncio
import logging
from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.medium import MediumScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "atacanymc"
    try:
        logger.info(f"Fetching Medium articles for: {username}")
        medium_scraper = MediumScraper()
        medium_data = await medium_scraper.fetch_data(username)
        logger.info(f"Medium success: {len(medium_data)} articles found.")
        for article in medium_data[:3]:
            logger.info(f"- {article.title}")
    except ScraperError as e:
        logger.error(f"Medium scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
