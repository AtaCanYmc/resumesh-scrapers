"""
03_custom_provider_plugin.py
============================
Tutorial demonstrating how third-party developers can create a custom platform
provider (e.g. KaggleProvider) by extending BaseProvider and registering it
dynamically into ProviderRegistry.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

from resumesh_scrapers import (
    Article,
    BaseProvider,
    Profile,
    Project,
    registry,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# 1. Custom Parser
class KaggleParser:
    """Parses raw Kaggle profile or dataset response payloads."""

    @staticmethod
    def parse_user(raw: dict[str, Any]) -> dict[str, Any]:
        return {
            "username": raw.get("userName", ""),
            "name": raw.get("displayName"),
            "bio": raw.get("bio"),
            "avatar_url": raw.get("userAvatarUrl"),
            "tier": raw.get("tier"),
        }

    @staticmethod
    def parse_dataset(raw: dict[str, Any]) -> dict[str, Any]:
        return {
            "title": raw.get("title", ""),
            "url": f"https://www.kaggle.com/datasets/{raw.get('ref', '')}",
            "upvotes": raw.get("voteCount", 0),
            "downloads": raw.get("downloadCount", 0),
        }


# 2. Custom Mapper
class KaggleMapper:
    """Maps parsed Kaggle data to normalized Profile and Project domain models."""

    @staticmethod
    def to_profile(parsed: dict[str, Any]) -> Profile:
        return Profile(
            platform="kaggle",
            username=parsed.get("username", ""),
            name=parsed.get("name"),
            bio=parsed.get("bio"),
            avatar_url=parsed.get("avatar_url"),
            website=f"https://www.kaggle.com/{parsed.get('username')}",
            social_links={"kaggle": f"https://www.kaggle.com/{parsed.get('username')}"},
            raw_extra={"tier": parsed.get("tier")},
        )

    @staticmethod
    def to_project(parsed: dict[str, Any]) -> Project:
        return Project(
            platform="kaggle",
            name=parsed.get("title", ""),
            url=parsed.get("url", ""),
            stars=parsed.get("upvotes", 0),
            topics=["dataset", "data-science"],
            raw_extra={"downloads": parsed.get("downloads", 0)},
        )


# 3. Custom BaseProvider Implementation
class KaggleProvider(BaseProvider):
    """Custom 3rd-party Kaggle Data Provider."""

    PLATFORM_NAME = "kaggle"

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        cache_key = f"kaggle:profile:{identifier}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Simulated Kaggle raw data fetch
        raw = {
            "userName": identifier,
            "displayName": "Kaggle Grandmaster",
            "bio": "Data Scientist & ML Engineer",
            "userAvatarUrl": "https://www.kaggle.com/avatar.jpg",
            "tier": "Grandmaster",
        }
        parsed = KaggleParser.parse_user(raw)
        profile = KaggleMapper.to_profile(parsed)
        await self.cache.set(cache_key, profile)
        return profile

    async def get_projects(self, identifier: str) -> list[Project]:
        cache_key = f"kaggle:datasets:{identifier}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        raw_datasets = [
            {
                "title": "Global Climate Dataset 2024",
                "ref": f"{identifier}/climate-2024",
                "voteCount": 142,
                "downloadCount": 3500,
            },
            {
                "title": "NLP Sentiment Analysis Corpus",
                "ref": f"{identifier}/nlp-corpus",
                "voteCount": 89,
                "downloadCount": 1200,
            },
        ]
        projects = [KaggleMapper.to_project(KaggleParser.parse_dataset(d)) for d in raw_datasets]
        await self.cache.set(cache_key, projects)
        return projects

    async def get_articles(self, identifier: str) -> list[Article]:
        return []


async def main() -> None:
    logger.info("=== 03. Custom Provider Plugin Demo ===")

    # 4. Register custom provider in central registry
    registry.register("kaggle", KaggleProvider)

    # 5. Verify registered provider list
    logger.info("Updated Provider Registry: %s", registry.list_providers())

    # 6. Retrieve and use KaggleProvider via standard registry API
    kaggle: Optional[KaggleProvider] = registry.get_provider("kaggle")  # type: ignore[assignment]
    if kaggle:
        profile = await kaggle.get_profile("datascience_pro")
        if profile:
            logger.info(
                "Fetched Custom Profile: %s (@%s) [Tier: %s]",
                profile.name,
                profile.username,
                profile.raw_extra.get("tier"),
            )

        datasets = await kaggle.get_projects("datascience_pro")
        logger.info("Fetched %d Kaggle Datasets as Projects:", len(datasets))
        for dataset in datasets:
            logger.info("  - %s (%d upvotes) -> %s", dataset.name, dataset.stars, dataset.url)


if __name__ == "__main__":
    asyncio.run(main())
