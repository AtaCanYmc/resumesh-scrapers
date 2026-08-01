"""
YouTube Provider implementing BaseProvider contract.
"""

from typing import Optional

from resumesh_scrapers.domain import Article, Profile, Project, Video
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.youtube.mapper import YouTubeMapper
from resumesh_scrapers.providers.youtube.parser import YouTubeParser


class YouTubeProvider(BaseProvider):
    """YouTube Platform Data Provider."""

    PLATFORM_NAME = "youtube"

    async def get_videos(self, identifier: str) -> list[Video]:
        cache_key = f"youtube:videos:{identifier}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        parsed = await YouTubeParser.parse_video_url(identifier)
        video = YouTubeMapper.to_video(parsed)
        videos = [video]
        await self.cache.set(cache_key, videos)
        return videos

    async def get_articles(self, identifier: str) -> list[Article]:
        return []

    async def get_profile(self, identifier: str) -> Optional[Profile]:
        return YouTubeMapper.to_profile(identifier)

    async def get_projects(self, identifier: str) -> list[Project]:
        return []
