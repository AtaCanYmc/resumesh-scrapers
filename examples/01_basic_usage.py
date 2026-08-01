"""
01_basic_usage.py
=================
Quick start example demonstrating basic profile, project, article, and video
retrieval using normalized domain models and global provider registry.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from resumesh_scrapers import (
    Article,
    DevToProvider,
    GitHubProvider,
    MediumProvider,
    Profile,
    Project,
    Video,
    YouTubeProvider,
    registry,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("=== 01. Basic Usage Demo ===")

    # 1. Inspect registered providers in registry
    providers = registry.list_providers()
    logger.info("Available Providers (%d): %s", len(providers), ", ".join(providers))

    # 2. Fetch GitHub Profile and Repositories
    github: Optional[GitHubProvider] = registry.get_provider("github")  # type: ignore[assignment]
    if github:
        profile: Optional[Profile] = await github.get_profile("octocat")
        if profile:
            logger.info("GitHub User: %s (@%s)", profile.name, profile.username)
            logger.info("Bio: %s | Location: %s", profile.bio, profile.location)

        projects: list[Project] = await github.get_projects("octocat")
        logger.info("Fetched %d normalized projects from GitHub:", len(projects))
        for proj in projects[:3]:
            logger.info("  - %s (%d ★ | %s): %s", proj.name, proj.stars, proj.language, proj.url)

    # 3. Fetch Dev.to Articles
    devto: Optional[DevToProvider] = registry.get_provider("devto")  # type: ignore[assignment]
    if devto:
        articles: list[Article] = await devto.get_articles("atacanymc")
        logger.info("Fetched %d articles from Dev.to:", len(articles))
        for art in articles[:3]:
            logger.info("  - %s (%s min read) -> %s", art.title, art.reading_time_minutes, art.url)

    # 4. Fetch Medium Articles
    medium: Optional[MediumProvider] = registry.get_provider("medium")  # type: ignore[assignment]
    if medium:
        medium_posts: list[Article] = await medium.get_articles("atacanymc")
        logger.info("Fetched %d posts from Medium:", len(medium_posts))
        for post in medium_posts[:3]:
            logger.info("  - %s -> %s", post.title, post.url)

    # 5. Fetch YouTube Video Metadata
    youtube: Optional[YouTubeProvider] = registry.get_provider("youtube")  # type: ignore[assignment]
    if youtube:
        videos: list[Video] = await youtube.get_videos("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        if videos:
            vid = videos[0]
            logger.info("YouTube Video: %s (%ds | %s views)", vid.title, vid.duration_seconds, vid.view_count)


if __name__ == "__main__":
    asyncio.run(main())
