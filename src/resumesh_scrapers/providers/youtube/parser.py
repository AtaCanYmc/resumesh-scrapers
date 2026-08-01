"""
YouTube video metadata parser using yt-dlp.
"""

import asyncio
from typing import Any
import yt_dlp
from resumesh_scrapers.exceptions import YouTubeScraperError


class YouTubeParser:
    """Extracts metadata from YouTube video URLs."""

    @staticmethod
    def _extract_sync(url: str) -> dict[str, Any]:
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
                    raise YouTubeScraperError("Failed to extract video info")
                return info
        except Exception as exc:
            if isinstance(exc, YouTubeScraperError):
                raise
            raise YouTubeScraperError(f"yt-dlp extraction error: {exc}") from exc

    @classmethod
    async def parse_video_url(cls, url: str) -> dict[str, Any]:
        info = await asyncio.to_thread(cls._extract_sync, url)
        if not info.get("url"):
            info["url"] = info.get("webpage_url") or url
        return info
