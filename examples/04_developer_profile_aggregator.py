"""
04_developer_profile_aggregator.py
==================================
Production-grade profile aggregator script concurrently harvesting developer profile
data across GitHub, Dev.to, Medium, Substack, Behance, NPM, PyPI, and YouTube
and merging all normalized entities into a unified JSON resume payload.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Optional

from pydantic import BaseModel, Field
from resumesh_scrapers import (
    Article,
    BaseProvider,
    Profile,
    Project,
    Video,
    registry,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class UnifiedDeveloperResume(BaseModel):
    """Unified Developer Portfolio & Resume Payload."""

    primary_profile: Optional[Profile] = None
    profiles: list[Profile] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    articles: list[Article] = Field(default_factory=list)
    videos: list[Video] = Field(default_factory=list)


async def safe_fetch_profile(provider: BaseProvider, identifier: str) -> Optional[Profile]:
    try:
        return await provider.get_profile(identifier)
    except Exception as exc:
        logger.warning("[%s] Profile fetch skipped due to error: %s", provider.PLATFORM_NAME, exc)
        return None


async def safe_fetch_projects(provider: BaseProvider, identifier: str) -> list[Project]:
    try:
        return await provider.get_projects(identifier)
    except Exception as exc:
        logger.warning("[%s] Projects fetch skipped due to error: %s", provider.PLATFORM_NAME, exc)
        return []


async def safe_fetch_articles(provider: BaseProvider, identifier: str) -> list[Article]:
    try:
        return await provider.get_articles(identifier)
    except Exception as exc:
        logger.warning("[%s] Articles fetch skipped due to error: %s", provider.PLATFORM_NAME, exc)
        return []


async def safe_fetch_videos(provider: BaseProvider, identifier: str) -> list[Video]:
    try:
        return await provider.get_videos(identifier)
    except Exception as exc:
        logger.warning("[%s] Videos fetch skipped due to error: %s", provider.PLATFORM_NAME, exc)
        return []


async def aggregate_developer_profile(handles: dict[str, str]) -> UnifiedDeveloperResume:
    logger.info("Starting concurrent profile aggregation for handles: %s", handles)

    tasks: list[Any] = []
    task_keys: list[tuple[str, str]] = []

    for platform, identifier in handles.items():
        provider = registry.get_provider(platform)
        if not provider:
            logger.warning("Provider '%s' not registered, skipping.", platform)
            continue

        tasks.append(safe_fetch_profile(provider, identifier))
        task_keys.append((platform, "profile"))

        tasks.append(safe_fetch_projects(provider, identifier))
        task_keys.append((platform, "projects"))

        tasks.append(safe_fetch_articles(provider, identifier))
        task_keys.append((platform, "articles"))

        tasks.append(safe_fetch_videos(provider, identifier))
        task_keys.append((platform, "videos"))

    results = await asyncio.gather(*tasks)

    resume = UnifiedDeveloperResume()

    for (platform, entity_type), result in zip(task_keys, results):
        if not result:
            continue
        if entity_type == "profile" and isinstance(result, Profile):
            resume.profiles.append(result)
            if platform == "github":
                resume.primary_profile = result
        elif entity_type == "projects" and isinstance(result, list):
            resume.projects.extend(result)
        elif entity_type == "articles" and isinstance(result, list):
            resume.articles.extend(result)
        elif entity_type == "videos" and isinstance(result, list):
            resume.videos.extend(result)

    if not resume.primary_profile and resume.profiles:
        resume.primary_profile = resume.profiles[0]

    return resume


async def main() -> None:
    logger.info("=== 04. Developer Profile Aggregator Demo ===")

    developer_handles = {
        "github": "octocat",
        "devto": "atacanymc",
        "medium": "atacanymc",
        "substack": "atacan",
        "behance": "atacanymc",
        "npm": "atacanymc",
        "pypi": "resumesh-scrapers",
        "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }

    resume = await aggregate_developer_profile(developer_handles)

    logger.info("==================================================")
    logger.info("Aggregated Resume Summary:")
    if resume.primary_profile:
        logger.info("Primary Developer: %s (@%s)", resume.primary_profile.name, resume.primary_profile.username)
    logger.info("Total Linked Profiles: %d", len(resume.profiles))
    logger.info("Total Normalized Projects: %d", len(resume.projects))
    logger.info("Total Articles/Posts: %d", len(resume.articles))
    logger.info("Total Videos: %d", len(resume.videos))
    logger.info("==================================================")

    # Export to clean JSON
    json_output = json.dumps(resume.model_dump(mode="json"), indent=2, default=str)
    logger.info("Generated JSON Portfolio Payload Preview (first 400 chars):\n%s...", json_output[:400])


if __name__ == "__main__":
    asyncio.run(main())
