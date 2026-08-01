"""
GitHub API raw response parser.
"""

from typing import Any


class GitHubParser:
    """Parses raw GitHub REST API payloads."""

    @staticmethod
    def parse_user(raw: dict[str, Any]) -> dict[str, Any]:
        """Extract user profile attributes."""
        return {
            "username": raw.get("login", ""),
            "name": raw.get("name"),
            "bio": raw.get("bio"),
            "avatar_url": raw.get("avatar_url"),
            "location": raw.get("location"),
            "company": raw.get("company"),
            "blog": raw.get("blog"),
            "public_repos": raw.get("public_repos", 0),
            "followers": raw.get("followers", 0),
            "following": raw.get("following", 0),
            "raw_data": raw,
        }

    @staticmethod
    def parse_repo(raw: dict[str, Any]) -> dict[str, Any]:
        """Extract repository attributes."""
        return {
            "name": raw.get("name", ""),
            "full_name": raw.get("full_name", ""),
            "description": raw.get("description"),
            "html_url": raw.get("html_url", ""),
            "stargazers_count": raw.get("stargazers_count", 0),
            "forks_count": raw.get("forks_count", 0),
            "language": raw.get("language"),
            "topics": raw.get("topics", []),
            "created_at": raw.get("created_at"),
            "updated_at": raw.get("updated_at"),
            "fork": raw.get("fork", False),
            "raw_data": raw,
        }
