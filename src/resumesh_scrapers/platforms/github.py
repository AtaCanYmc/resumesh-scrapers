"""
GitHub Scraper Service
========================
Fetches the user's public repositories from GitHub REST API
and returns them as ``ScrapedProject`` models.

Usage:
    from resumesh_scrapers import GitHubScraperService

    scraper = GitHubScraperService()
    projects = await scraper.fetch_data(
        username="octocat",
        pat="ghp_...",          # optional — rate limit 60 → 5000/hour
    )

API Reference:
    GET https://api.github.com/users/{username}/repos
    Docs: https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user
"""

import logging
import re
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Optional

from resumesh_scrapers.core.client import fetch_url
from resumesh_scrapers.exceptions import GitHubScraperError
from resumesh_scrapers.models import (
    GitHubCommitModel,
    GitHubRepositoryModel,
    GitHubUserModel,
)

from resumesh_scrapers.platforms.base import IScraperService

logger = logging.getLogger(__name__)

_GITHUB_API_BASE = "https://api.github.com"
_DEFAULT_TIMEOUT = 15.0
_DEFAULT_PER_PAGE = 100


class GitHubScraperService(IScraperService):
    """
    Service that fetches repository data using the GitHub REST API.
    """

    @staticmethod
    def _build_headers(pat: Optional[str] = None) -> dict[str, str]:
        """
        Creates HTTP headers for GitHub API.

        Args:
            pat: GitHub Personal Access Token (optional).
                 If provided, rate limit becomes 5000/hour instead of 60/hour.

        Returns:
            Header dict. `User-Agent` is always included.
        """
        headers: dict[str, str] = {"User-Agent": "ResuMesh-App"}
        if pat:
            headers["Authorization"] = f"Bearer {pat}"
        return headers

    @staticmethod
    def _parse_repo(raw: dict) -> GitHubRepositoryModel:
        """
        Converts a single repository dict from GitHub API to ``GitHubRepositoryModel``
        and handles auxiliary fields like languages and custom tags.
        """
        language = raw.get("language")
        languages = [language] if language else []

        tags = raw.get("topics", [])
        if not language and "no-lang-repo" not in tags:
            tags.append("no-lang-repo")
        elif language and not tags:
            tags.append(raw.get("name", "").lower())

        parsed_data = {
            **raw,
            "languages": languages,
            "tags": tags,
        }
        return GitHubRepositoryModel(**parsed_data)

    async def fetch_data(self, username: str, **kwargs) -> list[GitHubRepositoryModel]:
        pat = kwargs.get("pat")
        include_forks = kwargs.get("include_forks", False)
        """
        Fetches the user's GitHub repositories
        and returns a list of ``ScrapedProject`` objects.

        Args:
            username: GitHub username.
            pat: Personal Access Token (optional).
            include_forks: If True, fork repositories are also included.
                           Default is False — only original repositories.

        Returns:
            List of ``ScrapedProject`` objects.

        Raises:
            GitHubScraperError: If API request fails (4xx / 5xx or network error)
                                or if the username is invalid.
        """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise GitHubScraperError("Invalid GitHub username format.")

        url = f"{_GITHUB_API_BASE}/users/{username}/repos?per_page={_DEFAULT_PER_PAGE}&sort=updated"
        headers = GitHubScraperService._build_headers(pat)

        logger.info("[GITHUB] Fetching repos for user=%s", username)

        response = await fetch_url(
            url=url,
            headers=headers,
            timeout=_DEFAULT_TIMEOUT,
            error_class=GitHubScraperError,
            platform_name="GITHUB",
        )

        raw_repos: list[dict] = response.json()
        logger.info("[GITHUB] Received %d repos for user=%s", len(raw_repos), username)

        projects: list[GitHubRepositoryModel] = []
        for raw in raw_repos:
            if not include_forks and raw.get("fork"):
                continue
            projects.append(GitHubScraperService._parse_repo(raw))

        logger.info(
            "[GITHUB] Parsed %d repos (include_forks=%s) for user=%s",
            len(projects),
            include_forks,
            username,
        )
        return projects

    async def fetch_readme_repo(self, username: str, **kwargs) -> Optional[GitHubRepositoryModel]:
        """
        Fetches the user's special profile README repository (username/username).
        If the repository does not exist, returns None.

        Args:
            username: GitHub username.
            pat: Personal Access Token (optional).

        Returns:
            GitHubRepositoryModel if repository exists, otherwise None.

        Raises:
            GitHubScraperError: If API request fails with a status code other than 404.
        """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise GitHubScraperError("Invalid GitHub username format.")

        pat = kwargs.get("pat")
        url = f"{_GITHUB_API_BASE}/repos/{username}/{username}"
        headers = GitHubScraperService._build_headers(pat)

        logger.info("[GITHUB] Fetching README repo for user=%s", username)

        try:
            response = await fetch_url(
                url=url,
                headers=headers,
                timeout=_DEFAULT_TIMEOUT,
                error_class=GitHubScraperError,
                platform_name="GITHUB",
            )
        except GitHubScraperError as exc:
            if exc.status_code == 404:
                logger.info("[GITHUB] README repo not found for user=%s", username)
                return None
            raise

        raw_repo = response.json()
        return GitHubScraperService._parse_repo(raw_repo)

    @staticmethod
    def _parse_commit(raw_item: dict) -> GitHubCommitModel:
        """
        Converts a single commit item search response into ``GitHubCommitModel``.
        """
        sha = raw_item.get("sha", "")
        commit_data = raw_item.get("commit", {})
        author_data = commit_data.get("author", {})
        repo_data = raw_item.get("repository", {})

        date_str = author_data.get("date")
        if date_str:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            date = datetime.now(timezone.utc)

        return GitHubCommitModel(
            sha=sha,
            message=commit_data.get("message", ""),
            author_name=author_data.get("name", ""),
            author_email=author_data.get("email", ""),
            date=date,
            repo_name=repo_data.get("name", ""),
            repo_full_name=repo_data.get("full_name", ""),
            html_url=raw_item.get("html_url", ""),
        )

    async def fetch_commits(self, username: str, **kwargs) -> list[GitHubCommitModel]:
        """
        Fetches the user's GitHub commits.

        Args:
            username: GitHub username.
            pat: Personal Access Token (optional).
            since: datetime or ISO string (optional). Defaults to 7 days ago.
            until: datetime or ISO string (optional).

        Returns:
            List of ``GitHubCommitModel`` objects.

        Raises:
            GitHubScraperError: If API request fails.
        """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise GitHubScraperError("Invalid GitHub username format.")

        pat = kwargs.get("pat")
        since = kwargs.get("since")
        until = kwargs.get("until")

        # Default to 7 days ago
        if not since:
            since_dt = datetime.now(timezone.utc) - timedelta(days=7)
            since_str = since_dt.isoformat()
        elif isinstance(since, datetime):
            since_str = since.isoformat()
        else:
            since_str = str(since)

        query = f"author:{username} author-date:>={since_str}"

        if until:
            if isinstance(until, datetime):
                until_str = until.isoformat()
            else:
                until_str = str(until)
            query += f" author-date:<={until_str}"

        params = {"q": query, "sort": "author-date", "order": "desc", "per_page": "100"}
        encoded_query = urllib.parse.urlencode(params)
        url = f"{_GITHUB_API_BASE}/search/commits?{encoded_query}"
        # We need commit search media type, but for repos we only need standard.
        # Let's request application/vnd.github+json which works for commits as well as repos.
        headers = {
            "User-Agent": "ResuMesh-App",
            "Accept": "application/vnd.github+json",
        }
        if pat:
            headers["Authorization"] = f"Bearer {pat}"

        logger.info("[GITHUB] Fetching commits for user=%s, since=%s", username, since_str)

        response = await fetch_url(
            url=url,
            headers=headers,
            timeout=_DEFAULT_TIMEOUT,
            error_class=GitHubScraperError,
            platform_name="GITHUB_COMMITS",
        )

        raw_data = response.json()
        items = raw_data.get("items", [])
        logger.info("[GITHUB] Received %d commits for user=%s", len(items), username)

        return [GitHubScraperService._parse_commit(item) for item in items]

    async def fetch_followers(self, username: str, **kwargs) -> list[GitHubUserModel]:
        """
        Fetches the user's followers list.

        Args:
            username: GitHub username.
            pat: Personal Access Token (optional).
            per_page: Results per page (optional, default 100).

        Returns:
            List of ``GitHubUserModel`` objects.

        Raises:
            GitHubScraperError: If API request fails.
        """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise GitHubScraperError("Invalid GitHub username format.")

        pat = kwargs.get("pat")
        per_page = kwargs.get("per_page", 100)

        url = f"{_GITHUB_API_BASE}/users/{username}/followers?per_page={per_page}"
        headers = GitHubScraperService._build_headers(pat)

        logger.info("[GITHUB] Fetching followers for user=%s", username)

        response = await fetch_url(
            url=url,
            headers=headers,
            timeout=_DEFAULT_TIMEOUT,
            error_class=GitHubScraperError,
            platform_name="GITHUB",
        )

        raw_users = response.json()
        return [GitHubUserModel(**raw) for raw in raw_users]

    async def fetch_following(self, username: str, **kwargs) -> list[GitHubUserModel]:
        """
        Fetches the list of users that the target user follows.

        Args:
            username: GitHub username.
            pat: Personal Access Token (optional).
            per_page: Results per page (optional, default 100).

        Returns:
            List of ``GitHubUserModel`` objects.

        Raises:
            GitHubScraperError: If API request fails.
        """
        if not re.match(r"^[a-zA-Z0-9\-]+$", username):
            raise GitHubScraperError("Invalid GitHub username format.")

        pat = kwargs.get("pat")
        per_page = kwargs.get("per_page", 100)

        url = f"{_GITHUB_API_BASE}/users/{username}/following?per_page={per_page}"
        headers = GitHubScraperService._build_headers(pat)

        logger.info("[GITHUB] Fetching following list for user=%s", username)

        response = await fetch_url(
            url=url,
            headers=headers,
            timeout=_DEFAULT_TIMEOUT,
            error_class=GitHubScraperError,
            platform_name="GITHUB",
        )

        raw_users = response.json()
        return [GitHubUserModel(**raw) for raw in raw_users]


# Alias for backward compatibility
GitHubScraper = GitHubScraperService

