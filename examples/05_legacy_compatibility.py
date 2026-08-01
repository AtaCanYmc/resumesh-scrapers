"""
05_legacy_compatibility.py
==========================
Demonstrates backward compatibility for legacy scraper services (GitHubScraper,
DevToScraper, MediumScraper, BehanceScraper, NpmScraper, PyPIScraper, YouTubeScraper)
for projects transitioning from older versions of resumesh-scrapers.
"""

from __future__ import annotations

import asyncio
import logging

from resumesh_scrapers import (
    BehanceProjectModel,
    BehanceScraper,
    DevToArticleModel,
    DevToScraper,
    GitHubRepositoryModel,
    GitHubScraper,
    MediumEntryModel,
    MediumScraper,
    NpmScraper,
    NpmSearchResultModel,
    PyPiPackageModel,
    PyPIScraper,
    YouTubeScraper,
    YouTubeVideoModel,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("=== 05. Legacy Compatibility Scrapers Demo ===")

    # 1. GitHubScraper (Legacy Service)
    github_scraper = GitHubScraper()
    repos: list[GitHubRepositoryModel] = await github_scraper.fetch_data("octocat", include_forks=False)
    logger.info("[Legacy GitHubScraper] Fetched %d raw repository models.", len(repos))
    if repos:
        logger.info("  Sample: %s -> %s", repos[0].name, repos[0].html_url)

    # 2. DevToScraper (Legacy Service)
    devto_scraper = DevToScraper()
    devto_articles: list[DevToArticleModel] = await devto_scraper.fetch_data("atacanymc")
    logger.info("[Legacy DevToScraper] Fetched %d raw article models.", len(devto_articles))

    # 3. MediumScraper (Legacy Service)
    medium_scraper = MediumScraper()
    medium_entries: list[MediumEntryModel] = await medium_scraper.fetch_data("atacanymc")
    logger.info("[Legacy MediumScraper] Fetched %d raw entry models.", len(medium_entries))

    # 4. BehanceScraper (Legacy Service)
    behance_scraper = BehanceScraper()
    behance_projects: list[BehanceProjectModel] = await behance_scraper.fetch_data("atacanymc")
    logger.info("[Legacy BehanceScraper] Fetched %d raw project models.", len(behance_projects))

    # 5. NpmScraper (Legacy Service)
    npm_scraper = NpmScraper()
    npm_results: list[NpmSearchResultModel] = await npm_scraper.fetch_data("atacanymc")
    logger.info("[Legacy NpmScraper] Fetched %d npm search result objects.", len(npm_results))

    # 6. PyPIScraper (Legacy Service)
    pypi_scraper = PyPIScraper()
    pypi_pkgs: list[PyPiPackageModel] = await pypi_scraper.fetch_data("atacanymc", package_names=["resumesh-scrapers"])
    logger.info("[Legacy PyPIScraper] Fetched %d PyPI package models.", len(pypi_pkgs))

    # 7. YouTubeScraper (Legacy Service)
    youtube_scraper = YouTubeScraper()
    yt_videos: list[YouTubeVideoModel] = await youtube_scraper.fetch_data("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    logger.info("[Legacy YouTubeScraper] Fetched %d video models.", len(yt_videos))


if __name__ == "__main__":
    asyncio.run(main())
