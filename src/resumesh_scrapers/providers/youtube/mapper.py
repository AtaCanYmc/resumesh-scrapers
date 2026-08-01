"""
YouTube raw parsed metadata mapper to Video and Profile domain models.
"""

from typing import Any

from resumesh_scrapers.domain import Profile, Video


class YouTubeMapper:
    """Maps YouTube video metadata to Video and Profile domain models."""

    @staticmethod
    def to_video(parsed_video: dict[str, Any]) -> Video:
        tags = parsed_video.get("tags") or parsed_video.get("categories") or []

        return Video(
            platform="youtube",
            title=parsed_video.get("title", ""),
            url=parsed_video.get("url") or parsed_video.get("webpage_url") or "",
            description=parsed_video.get("description"),
            duration_seconds=parsed_video.get("duration"),
            view_count=parsed_video.get("view_count", 0),
            like_count=parsed_video.get("like_count", 0),
            thumbnail_url=parsed_video.get("thumbnail"),
            tags=tags,
            raw_extra=parsed_video,
        )

    @staticmethod
    def to_profile(channel_username_or_url: str) -> Profile:
        clean = channel_username_or_url.strip("@")
        if not clean.startswith("http"):
            url = f"https://www.youtube.com/@{clean}"
        else:
            url = clean
        return Profile(
            platform="youtube",
            username=clean,
            website=url,
            social_links={"youtube": url},
        )
