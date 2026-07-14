"""
resumesh-scrapers
=================
Standalone, reusable web scraping services for GitHub, Dev.to, and Medium.

Quick start::

    from resumesh_scrapers import GitHubScraperService, ScrapedProject

    scraper = GitHubScraperService()
    projects: list[ScrapedProject] = await scraper.fetch_data("octocat")
"""

from resumesh_scrapers._version import __version__
from resumesh_scrapers.base import IScraperService
from resumesh_scrapers.devto_scraper import DevToScraper, DevToScraperService
from resumesh_scrapers.exceptions import (
    DevToScraperError,
    GitHubScraperError,
    MediumScraperError,
    ScraperError,
)
from resumesh_scrapers.github_scraper import GitHubScraper, GitHubScraperService
from resumesh_scrapers.medium_scraper import MediumScraper, MediumScraperService
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle, ScrapedProject

__all__ = [
    # Version
    "__version__",
    # Base
    "IScraperService",
    # Scrapers
    "GitHubScraperService",
    "GitHubScraper",
    "DevToScraperService",
    "DevToScraper",
    "MediumScraperService",
    "MediumScraper",
    # Models
    "ScrapedProject",
    "ScrapedArticle",
    "ArticlePlatform",
    # Exceptions
    "ScraperError",
    "GitHubScraperError",
    "DevToScraperError",
    "MediumScraperError",
]
