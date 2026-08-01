"""
Medium raw parsed data mapper to Article and Profile domain models.
"""

from datetime import datetime
from typing import Any

from resumesh_scrapers.domain import Article, Profile


class MediumMapper:
    """Maps parsed Medium RSS data to Article and Profile domain models."""

    @staticmethod
    def to_article(parsed_entry: dict[str, Any]) -> Article:
        pub_at = None
        if parsed_entry.get("published_at"):
            try:
                # Handle RFC 822 or ISO date formats
                pub_at = datetime.fromisoformat(parsed_entry["published_at"])
            except Exception:
                pass

        return Article(
            platform="medium",
            title=parsed_entry.get("title", ""),
            url=parsed_entry.get("url", ""),
            summary=parsed_entry.get("summary"),
            published_at=pub_at,
            tags=parsed_entry.get("tags", []),
            raw_extra=parsed_entry.get("raw_data", {}),
        )

    @staticmethod
    def to_profile(username: str) -> Profile:
        clean_user = username.lstrip("@")
        return Profile(
            platform="medium",
            username=clean_user,
            website=f"https://medium.com/@{clean_user}",
            social_links={
                "medium": f"https://medium.com/@{clean_user}",
            },
        )
