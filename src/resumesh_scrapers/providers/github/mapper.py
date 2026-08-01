"""
GitHub raw parsed data to normalized domain models mapper.
"""

from datetime import datetime
from typing import Any, Optional
from resumesh_scrapers.domain import Profile, Project


class GitHubMapper:
    """Maps parsed GitHub data to Profile and Project domain models."""

    @staticmethod
    def to_profile(parsed_user: dict[str, Any]) -> Profile:
        website = parsed_user.get("blog")
        if website and not (website.startswith("http://") or website.startswith("https://")):
            website = f"https://{website}"

        return Profile(
            platform="github",
            username=parsed_user.get("username", ""),
            name=parsed_user.get("name"),
            bio=parsed_user.get("bio"),
            avatar_url=parsed_user.get("avatar_url"),
            location=parsed_user.get("location"),
            company=parsed_user.get("company"),
            website=website,
            social_links={
                "github": f"https://github.com/{parsed_user.get('username')}",
            },
            raw_extra=parsed_user.get("raw_data", {}),
        )

    @staticmethod
    def to_project(parsed_repo: dict[str, Any]) -> Project:
        created_at = None
        if parsed_repo.get("created_at"):
            try:
                created_at = datetime.fromisoformat(parsed_repo["created_at"].replace("Z", "+00:00"))
            except Exception:
                pass

        updated_at = None
        if parsed_repo.get("updated_at"):
            try:
                updated_at = datetime.fromisoformat(parsed_repo["updated_at"].replace("Z", "+00:00"))
            except Exception:
                pass

        return Project(
            platform="github",
            name=parsed_repo.get("name", ""),
            description=parsed_repo.get("description"),
            url=parsed_repo.get("html_url", ""),
            stars=parsed_repo.get("stargazers_count", 0),
            forks=parsed_repo.get("forks_count", 0),
            language=parsed_repo.get("language"),
            topics=parsed_repo.get("topics", []),
            created_at=created_at,
            updated_at=updated_at,
            raw_extra=parsed_repo.get("raw_data", {}),
        )
