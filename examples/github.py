import asyncio
import logging

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.github import GitHubScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "atacanymc"
    try:
        logger.info(f"Fetching GitHub data for: {username}")
        github_scraper = GitHubScraper()
        github_data = await github_scraper.fetch_data(username)
        logger.info(f"GitHub success: {len(github_data)} repositories found.")
        for repo in github_data[:3]:
            logger.info(f"- {repo.name} (Stars: {repo.stargazers_count})")
    except ScraperError as e:
        logger.error(f"GitHub scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
