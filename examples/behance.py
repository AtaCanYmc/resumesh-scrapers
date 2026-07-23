import asyncio
import logging

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.behance import BehanceScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "atacanymc"
    try:
        logger.info(f"Fetching Behance projects for: {username}")
        behance_scraper = BehanceScraper()
        behance_data = await behance_scraper.fetch_data(username)
        logger.info(f"Behance success: {len(behance_data)} projects found.")
        for project in behance_data[:3]:
            logger.info(f"- {project.name} (Appreciations: {project.stats_appreciations})")
    except ScraperError as e:
        logger.error(f"Behance scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
