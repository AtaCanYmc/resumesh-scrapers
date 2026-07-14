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
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from resumesh_scrapers.base import IScraperService
from resumesh_scrapers.exceptions import GitHubScraperError
from resumesh_scrapers.models import ScrapedProject

logger = logging.getLogger(__name__)

_GITHUB_API_BASE = "https://api.github.com"
_DEFAULT_TIMEOUT = 15.0
_DEFAULT_PER_PAGE = 100


class GitHubScraperService(IScraperService):
    """
    Service that fetches repository data using the GitHub REST API.
    """

    def _build_headers(pat: str | None = None) -> dict[str, str]:
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
    def _parse_repo(raw: dict[str, Any]) -> ScrapedProject:
        """
        Converts the raw repository dict from GitHub API to ``ScrapedProject``.

        Fork repositories do not reach this method;
        filtering is done inside ``fetch_data``.

        Args:
            raw: Single repository object returned by GitHub API.

        Returns:
            A ``ScrapedProject`` object.
        """
        primary_lang = raw.get("language")
        languages = [primary_lang] if primary_lang else []
        # Repo name is added as a lowercase tag, combined with language
        tags = list(set(languages + [raw["name"].lower()]))

        return ScrapedProject(
            title=raw["name"],
            description=raw.get("description"),
            github_url=raw["html_url"],
            stars=raw.get("stargazers_count", 0),
            watchers=raw.get("watchers_count", 0),
            forks=raw.get("forks_count", 0),
            languages=languages,
            tags=tags,
            raw_github_data=raw,
            created_at=raw.get("created_at"),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def fetch_data(self, username: str, **kwargs) -> list[ScrapedProject]:
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

        url = (
            f"{_GITHUB_API_BASE}/users/{username}/repos"
            f"?per_page={_DEFAULT_PER_PAGE}&sort=updated"
        )
        headers = GitHubScraperService._build_headers(pat)

        logger.info("[GITHUB] Fetching repos for user=%s", username)

        try:
            async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
                response = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            raise GitHubScraperError(
                f"Network error while fetching GitHub repos: {exc}"
            ) from exc

        if response.status_code != 200:
            raise GitHubScraperError(
                "GitHub API returned HTTP "
                f"{response.status_code} for user '{username}'."
                f" Response: {response.text[:300]}",
                status_code=response.status_code,
            )

        raw_repos: list[dict] = response.json()
        logger.info("[GITHUB] Received %d repos for user=%s", len(raw_repos), username)

        projects: list[ScrapedProject] = []
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


# Alias for backward compatibility
GitHubScraper = GitHubScraperService
