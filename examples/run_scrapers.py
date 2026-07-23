"""
Example usage script for resumesh-scrapers.
Demonstrates how to fetch user data from GitHub, Dev.to, and Medium platforms.
"""

import asyncio
import logging
from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.devto import DevToScraper
from resumesh_scrapers.platforms.github import GitHubScraper
from resumesh_scrapers.platforms.medium import MediumScraper

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    # Sample usernames / profiles
    github_username = "atacanymc"
    devto_username = "atacanymc"  # Sample profile
    medium_username = "atacanymc"  # Sample profile or RSS feed

    logger.info("Initializing scraper examples...")

    # 1. GitHub Example
    try:
        logger.info(f"Fetching GitHub data for: {github_username}")
        github_scraper = GitHubScraper()
        github_data = await github_scraper.fetch_data(github_username)
        logger.info(f"GitHub data successfully fetched: {github_data}")
    except ScraperError as e:
        logger.error(f"GitHub scraping error: {e}")

    # 2. Dev.to Example (Eğer bu fonksiyon senkron ise await kaldırılabilir)
    try:
        logger.info(f"Fetching Dev.to articles for: {devto_username}")
        devto_scraper = DevToScraper()
        # Eğer DevToScraper.fetch_data senkron ise: devto_data = devto_scraper.fetch_data(devto_username)
        # Eğer asenkron ise: devto_data = await devto_scraper.fetch_data(devto_username)
        devto_data = devto_scraper.fetch_data(devto_username)
        logger.info(f"Dev.to data successfully fetched: {devto_data}")
    except ScraperError as e:
        logger.error(f"Dev.to scraping error: {e}")

    # 3. Medium Example
    try:
        logger.info(f"Fetching Medium content for: {medium_username}")
        medium_scraper = MediumScraper()
        medium_data = await medium_scraper.fetch_data(medium_username)
        logger.info(f"Medium data successfully fetched: {medium_data}")
    except ScraperError as e:
        logger.error(f"Medium scraping error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
