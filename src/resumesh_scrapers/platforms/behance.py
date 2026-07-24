"""
Behance Scraper Service
========================
Fetches the creator's public projects from Behance profile pages
and returns them as ``BehanceProjectModel`` objects.

Usage:
    from resumesh_scrapers import BehanceScraperService

    scraper = BehanceScraperService()
    projects = await scraper.fetch_data(username="atacanymc")

API / Page Reference:
    GET https://www.behance.net/{username}
"""

import logging
import re
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from resumesh_scrapers.core.client import fetch_url
from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.models import BehanceProjectModel
from resumesh_scrapers.platforms.base import IScraperService

logger = logging.getLogger(__name__)

_BEHANCE_PROFILE_URL = "https://www.behance.net/{username}"
_DEFAULT_TIMEOUT = 15.0


class BehanceScraperError(ScraperError):
    """Raised when the Behance scraper encounters an error or invalid response."""


class BehanceScraperService(IScraperService):
    """
    Service that fetches and parses public projects from a Behance creator profile.
    """

    async def fetch_data(self, username: str, **kwargs) -> list[BehanceProjectModel]:
        """
        Fetches the creator's public projects from Behance.

        Args:
            username: Behance username/profile handle.

        Returns:
            List of ``BehanceProjectModel`` objects.

        Raises:
            BehanceScraperError: If the profile cannot be reached, HTTP error occurs,
                                 or if the username format is invalid.
        """
        api_key = kwargs.get("api_key") or kwargs.get("client_id")
        clean_user = username.strip("@")
        if not re.match(r"^[a-zA-Z0-9\-_]+$", clean_user):
            raise BehanceScraperError("Invalid Behance username format.")

        if api_key:
            return await self._fetch_via_api(clean_user, api_key)
        else:
            return await self._fetch_via_scraping(clean_user)

    async def _fetch_via_api(self, clean_user: str, api_key: str) -> list[BehanceProjectModel]:
        """Fetches and parses projects using the Behance v2 API."""
        api_url = f"https://api.behance.net/v2/users/{clean_user}/projects?api_key={api_key}"
        logger.info("[BEHANCE] Fetching API projects for user=%s", clean_user)
        response = await fetch_url(
            url=api_url,
            timeout=_DEFAULT_TIMEOUT,
            error_class=BehanceScraperError,
            platform_name="BEHANCE",
        )
        try:
            data = response.json()
            raw_projects = data.get("projects", [])
            projects = self._parse_api_projects(raw_projects)
            logger.info("[BEHANCE] Successfully parsed %d projects from API for user=%s", len(projects), clean_user)
            return projects
        except Exception as exc:
            raise BehanceScraperError(f"Failed to parse Behance API response: {exc}")

    def _parse_api_projects(self, raw_projects: list[dict]) -> list[BehanceProjectModel]:
        """Parses Behance API project data dicts into BehanceProjectModel objects."""
        projects: list[BehanceProjectModel] = []
        for proj in raw_projects:
            pub_on = proj.get("published_on")
            published_dt = None
            if pub_on is not None:
                try:
                    published_dt = datetime.fromtimestamp(float(pub_on), tz=timezone.utc)
                except Exception:
                    pass
            
            covers = proj.get("covers", {})
            covers_url = covers.get("original") or covers.get("max_808") or covers.get("404")
            
            projects.append(
                BehanceProjectModel(
                    id=str(proj.get("id")) if proj.get("id") else None,
                    name=proj.get("name", "Untitled Project"),
                    url=proj.get("url"),
                    published_on=published_dt,
                    stats_appreciations=proj.get("stats", {}).get("appreciations", 0),
                    stats_views=proj.get("stats", {}).get("views", 0),
                    covers_url=covers_url,
                    tags=proj.get("fields", []),
                )
            )
        return projects

    async def _fetch_via_scraping(self, clean_user: str) -> list[BehanceProjectModel]:
        """Fetches and parses projects from the Behance HTML profile page."""
        url = _BEHANCE_PROFILE_URL.format(username=clean_user)
        logger.info("[BEHANCE] Fetching profile page for user=%s", clean_user)

        response = await fetch_url(
            url=url,
            timeout=_DEFAULT_TIMEOUT,
            follow_redirects=True,
            error_class=BehanceScraperError,
            platform_name="BEHANCE",
        )

        try:
            projects = self._parse_html_projects(response.text)
            logger.info(
                "[BEHANCE] Successfully parsed %d projects for user=%s",
                len(projects),
                clean_user,
            )
            return projects
        except Exception as exc:
            raise BehanceScraperError(f"Failed to parse Behance profile page: {exc}")

    def _parse_html_projects(self, html_content: str) -> list[BehanceProjectModel]:
        """Parses project cards from raw HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        projects: list[BehanceProjectModel] = []
        seen_urls: set[str] = set()

        project_cards = soup.select("div.project-card, [class*='ProjectCover']")

        for card in project_cards:
            try:
                title_elem = card.select_one("a.projekt-link, [class*='Title'], [class*='title'], h3")
                title = title_elem.get_text(strip=True) if title_elem else "Untitled Project"

                link_elem = card.select_one("a[href*='/gallery/']")
                project_url = link_elem["href"] if link_elem and link_elem.has_attr("href") else None
                if project_url and not project_url.startswith("http"):
                    project_url = f"https://www.behance.net{project_url}"

                if not project_url:
                    continue

                if project_url in seen_urls:
                    continue
                seen_urls.add(project_url)

                appreciations = 0
                appr_elem = card.select_one(
                    "[class*='Appreciations'], [class*='appreciations'], [class*='Stat--appreciations']"
                )
                if appr_elem:
                    nums = re.findall(r"\d+", appr_elem.get_text())
                    if nums:
                        appreciations = int(nums[0])

                projects.append(
                    BehanceProjectModel(
                        name=title,
                        url=project_url,
                        stats_appreciations=appreciations,
                    )
                )
            except Exception as inner_exc:
                logger.warning(
                    "[BEHANCE] Skipping a project card due to parse error: %s",
                    inner_exc,
                )
                continue

        return projects


# Alias for backward compatibility
BehanceScraper = BehanceScraperService
