import asyncio
import logging
from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.pypi import PyPIScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "atacanymc"
    packages = ["resumesh-scrapers"]
    try:
        logger.info(f"Fetching PyPI packages for: {username} -> {packages}")
        pypi_scraper = PyPIScraper()
        pypi_data = await pypi_scraper.fetch_data(username, package_names=packages)
        logger.info(f"PyPI success: {len(pypi_data)} packages processed.")
        for pkg in pypi_data:
            logger.info(f"- {pkg.info.name} (v{pkg.info.version})")
    except ScraperError as e:
        logger.error(f"PyPI scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
