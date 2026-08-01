"""
Substack raw parsed data mapper to Article domain model.
"""

from datetime import datetime
from typing import Any
from resumesh_scrapers.domain import Article, Profile


class SubstackMapper:
    """Maps parsed Substack RSS data to Article and Profile domain models."""

    @staticmethod
    def to_article(parsed_entry: dict[str, Any]) -> Article:
        pub_at = None
        if parsed_entry.get("published_at"):
            try:
                pub_at = datetime.fromisoformat(parsed_entry["published_at"])
            except Exception:
                pass

        return Article(
            platform="substack",
            title=parsed_entry.get("title", ""),
            url=parsed_entry.get("url", ""),
            summary=parsed_entry.get("summary"),
            published_at=pub_at,
            raw_extra=parsed_entry.get("raw_data", {}),
        )

    @staticmethod
    def to_profile(publication_or_username: str) -> Profile:
        subdomain = publication_or_username.lower().replace(".substack.com", "").lstrip("@")
        return Profile(
            platform="substack",
            username=subdomain,
            website=f"https://{subdomain}.substack.com",
            social_links={
                "substack": f"https://{subdomain}.substack.com",
            },
        )
