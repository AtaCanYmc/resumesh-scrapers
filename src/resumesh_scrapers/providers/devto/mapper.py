"""
Dev.to raw parsed data mapper to Article and Profile domain models.
"""

from datetime import datetime
from typing import Any

from resumesh_scrapers.domain import Article, Profile


class DevToMapper:
    """Maps parsed Dev.to payload into Article and Profile domain models."""

    @staticmethod
    def to_article(parsed_article: dict[str, Any]) -> Article:
        pub_at = None
        if parsed_article.get("published_at"):
            try:
                pub_at = datetime.fromisoformat(parsed_article["published_at"].replace("Z", "+00:00"))
            except Exception:
                pass

        tags = parsed_article.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        return Article(
            platform="devto",
            title=parsed_article.get("title", ""),
            url=parsed_article.get("url", ""),
            summary=parsed_article.get("description"),
            content=parsed_article.get("body_markdown"),
            published_at=pub_at,
            tags=tags,
            reading_time_minutes=parsed_article.get("reading_time_minutes"),
            raw_extra=parsed_article.get("raw_data", {}),
        )

    @staticmethod
    def to_profile(parsed_user: dict[str, Any]) -> Profile:
        username = parsed_user.get("username", "")
        return Profile(
            platform="devto",
            username=username,
            name=parsed_user.get("name"),
            avatar_url=parsed_user.get("profile_image"),
            website=f"https://dev.to/{username}" if username else None,
            social_links={
                "devto": f"https://dev.to/{username}" if username else "",
            },
        )
