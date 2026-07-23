import asyncio
import logging
from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.npm import NpmScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "atacanymc"
    try:
        logger.info(f"Fetching npm packages for maintainer: {username}")
        npm_scraper = NpmScraper()
        npm_data = await npm_scraper.fetch_data(username)
        logger.info(f"npm success: {len(npm_data)} search results found.")
        for res in npm_data:
            for obj in res.objects:
                logger.info(f"- {obj.package.name} (v{obj.package.version})")
    except ScraperError as e:
        logger.error(f"npm scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
