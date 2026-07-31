"""
YouTube Scraper Service
=======================
Extracts YouTube video metadata using ``yt-dlp`` and returns a ``YouTubeVideoModel``.

Usage:
    from resumesh_scrapers import YouTubeScraperService

    scraper = YouTubeScraperService()
    video_data = await scraper.fetch_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
"""

import asyncio
import logging
from typing import Any, List

import yt_dlp

from resumesh_scrapers.exceptions import YouTubeScraperError
from resumesh_scrapers.models.youtube import YouTubeVideoModel
from resumesh_scrapers.platforms.base import IScraperService

logger = logging.getLogger(__name__)


class YouTubeScraperService(IScraperService):
    """
    Service that extracts metadata from a YouTube video URL using yt-dlp.
    """

    def _extract_info(self, url: str) -> dict[str, Any]:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise YouTubeScraperError("Failed to extract video information from the provided URL.")
                return info
        except Exception as exc:
            if isinstance(exc, YouTubeScraperError):
                raise
            raise YouTubeScraperError(f"yt-dlp extraction error: {exc}") from exc

    async def fetch_video(self, url: str) -> YouTubeVideoModel:
        """
        Fetches metadata for a single YouTube video URL.

        Args:
            url: YouTube video URL.

        Returns:
            ``YouTubeVideoModel`` object.
        """
        logger.info("[YOUTUBE] Extracting video metadata for url=%s", url)
        info = await asyncio.to_thread(self._extract_info, url)

        # Ensure webpage_url or original url is set if url field is empty
        if not info.get("url"):
            info["url"] = info.get("webpage_url") or url

        video_model = YouTubeVideoModel.model_validate(info)
        logger.info("[YOUTUBE] Successfully extracted video metadata: %s", video_model.title)
        return video_model

    async def fetch_data(self, username: str, **kwargs) -> List[YouTubeVideoModel]:
        """
        Implementation of IScraperService interface.
        Can be given a video URL via `url` kwarg or `username` parameter.
        """
        url = kwargs.get("url", username)
        video = await self.fetch_video(url)
        return [video]


# Alias for backward compatibility / consistency
YouTubeScraper = YouTubeScraperService
