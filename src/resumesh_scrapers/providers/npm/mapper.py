"""
NPM raw parsed data mapper to Project and Profile domain models.
"""

from datetime import datetime
from typing import Any
from resumesh_scrapers.domain import Profile, Project


class NpmMapper:
    """Maps parsed npm package metadata to Project and Profile domain models."""

    @staticmethod
    def to_project(parsed_pkg: dict[str, Any]) -> Project:
        links = parsed_pkg.get("links", {})
        pkg_url = links.get("npm") or f"https://www.npmjs.com/package/{parsed_pkg.get('name')}"

        updated_at = None
        if parsed_pkg.get("date"):
            try:
                updated_at = datetime.fromisoformat(parsed_pkg["date"].replace("Z", "+00:00"))
            except Exception:
                pass

        return Project(
            platform="npm",
            name=parsed_pkg.get("name", ""),
            description=parsed_pkg.get("description"),
            url=pkg_url,
            language="JavaScript",
            topics=parsed_pkg.get("keywords", []),
            updated_at=updated_at,
            raw_extra=parsed_pkg.get("raw_data", {}),
        )

    @staticmethod
    def to_profile(username: str) -> Profile:
        clean_user = username.strip("@")
        return Profile(
            platform="npm",
            username=clean_user,
            website=f"https://www.npmjs.com/~{clean_user}",
            social_links={
                "npm": f"https://www.npmjs.com/~{clean_user}",
            },
        )
