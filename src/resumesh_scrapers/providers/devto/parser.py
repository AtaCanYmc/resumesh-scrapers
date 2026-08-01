"""
Dev.to API raw response parser.
"""

from typing import Any


class DevToParser:
    """Parses raw Dev.to REST API payloads."""

    @staticmethod
    def parse_article(raw: dict[str, Any]) -> dict[str, Any]:
        """Extract raw article attributes."""
        user = raw.get("user", {})
        return {
            "title": raw.get("title", ""),
            "url": raw.get("url") or raw.get("canonical_url", ""),
            "description": raw.get("description"),
            "body_markdown": raw.get("body_markdown"),
            "published_at": raw.get("published_at"),
            "reading_time_minutes": raw.get("reading_time_minutes"),
            "tags": raw.get("tag_list") or raw.get("tags") or [],
            "user": {
                "username": user.get("username"),
                "name": user.get("name"),
                "profile_image": user.get("profile_image"),
            },
            "raw_data": raw,
        }
