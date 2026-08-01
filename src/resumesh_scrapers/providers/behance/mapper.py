"""
Behance raw parsed data mapper to Project and Profile domain models.
"""

from datetime import datetime, timezone
from typing import Any
from resumesh_scrapers.domain import Profile, Project


class BehanceMapper:
    """Maps parsed Behance project data to Project and Profile domain models."""

    @staticmethod
    def to_project(parsed: dict[str, Any]) -> Project:
        pub_on = parsed.get("published_on")
        created_at = None
        if pub_on is not None:
            try:
                created_at = datetime.fromtimestamp(float(pub_on), tz=timezone.utc)
            except Exception:
                pass

        return Project(
            platform="behance",
            name=parsed.get("name", "Untitled Project"),
            url=parsed.get("url") or "",
            stars=parsed.get("appreciations", 0),
            topics=parsed.get("tags", []),
            created_at=created_at,
            raw_extra=parsed.get("raw_data", {}),
        )

    @staticmethod
    def to_profile(username: str) -> Profile:
        clean_user = username.strip("@")
        return Profile(
            platform="behance",
            username=clean_user,
            website=f"https://www.behance.net/{clean_user}",
            social_links={
                "behance": f"https://www.behance.net/{clean_user}",
            },
        )
