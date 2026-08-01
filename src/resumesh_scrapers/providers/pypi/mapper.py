"""
PyPI raw parsed data mapper to Project and Profile domain models.
"""

from typing import Any
from resumesh_scrapers.domain import Profile, Project


class PyPiMapper:
    """Maps parsed PyPI package metadata to Project and Profile domain models."""

    @staticmethod
    def to_project(parsed_pkg: dict[str, Any]) -> Project:
        keywords = parsed_pkg.get("keywords") or ""
        topics = [k.strip() for k in keywords.split(",") if k.strip()] if isinstance(keywords, str) else []

        url = parsed_pkg.get("package_url") or parsed_pkg.get("home_page") or f"https://pypi.org/project/{parsed_pkg.get('name')}"

        return Project(
            platform="pypi",
            name=parsed_pkg.get("name", ""),
            description=parsed_pkg.get("summary"),
            url=url,
            language="Python",
            topics=topics,
            raw_extra=parsed_pkg.get("raw_data", {}),
        )

    @staticmethod
    def to_profile(username: str) -> Profile:
        clean_user = username.strip("@")
        return Profile(
            platform="pypi",
            username=clean_user,
            website=f"https://pypi.org/user/{clean_user}/",
            social_links={
                "pypi": f"https://pypi.org/user/{clean_user}/",
            },
        )
