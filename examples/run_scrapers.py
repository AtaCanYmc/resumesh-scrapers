"""
Example usage script for resumesh-scrapers.
Demonstrates how to fetch user data from GitHub, Dev.to, Medium, npm, and PyPI platforms.
"""

import asyncio
import logging
from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.devto import DevToScraper
from resumesh_scrapers.platforms.github import GitHubScraper
from resumesh_scrapers.platforms.medium import MediumScraper
from resumesh_scrapers.platforms.npm import NpmScraper
from resumesh_scrapers.platforms.pypi import PyPIScraper

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    # Sample usernames / identifiers
    github_username = "atacanymc"
    devto_username = "atacanymc"
    medium_username = "atacanymc"
    npm_username = "atacanymc"
    pypi_packages = ["resumesh-scrapers"]

    logger.info("Initializing scraper examples...")

    # 1. GitHub Example
    try:
        logger.info(f"Fetching GitHub data for: {github_username}")
        github_scraper = GitHubScraper()
        github_data = await github_scraper.fetch_data(github_username)
        logger.info(
            f"GitHub data successfully fetched: {len(github_data)} repositories found."
        )
    except ScraperError as e:
        logger.error(f"GitHub scraping error: {e}")

    # 2. Dev.to Example
    try:
        logger.info(f"Fetching Dev.to articles for: {devto_username}")
        devto_scraper = DevToScraper()
        devto_data = await devto_scraper.fetch_data(devto_username)
        logger.info(
            f"Dev.to data successfully fetched: {len(devto_data)} articles found."
        )
    except ScraperError as e:
        logger.error(f"Dev.to scraping error: {e}")

    # 3. Medium Example
    try:
        logger.info(f"Fetching Medium content for: {medium_username}")
        medium_scraper = MediumScraper()
        medium_data = await medium_scraper.fetch_data(medium_username)
        logger.info(
            f"Medium data successfully fetched: {len(medium_data)} articles found."
        )
    except ScraperError as e:
        logger.error(f"Medium scraping error: {e}")

    # 4. npm Example
    try:
        logger.info(f"Fetching npm packages for maintainer: {npm_username}")
        npm_scraper = NpmScraper()
        npm_data = await npm_scraper.fetch_data(npm_username)
        logger.info(f"npm data successfully fetched: {npm_data}")
    except ScraperError as e:
        logger.error(f"npm scraping error: {e}")

    # 5. PyPI Example
    try:
        logger.info(f"Fetching PyPI package metadata for packages: {pypi_packages}")
        pypi_scraper = PyPIScraper()
        pypi_data = await pypi_scraper.fetch_data(
            github_username, package_names=pypi_packages
        )
        logger.info(
            f"PyPI data successfully fetched: {len(pypi_data)} packages processed."
        )
    except ScraperError as e:
        logger.error(f"PyPI scraping error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
