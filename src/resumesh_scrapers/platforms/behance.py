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
        clean_user = username.strip("@")
        if not re.match(r"^[a-zA-Z0-9\-_]+$", clean_user):
            raise BehanceScraperError("Invalid Behance username format.")

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
            soup = BeautifulSoup(response.text, "html.parser")
            projects: list[BehanceProjectModel] = []

            # Target standard project cards on Behance profiles
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

                    # Extract appreciations/likes stats if available
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
                            published_on=datetime.now(timezone.utc),
                        )
                    )
                except Exception as inner_exc:
                    logger.warning(
                        "[BEHANCE] Skipping a project card due to parse error: %s",
                        inner_exc,
                    )
                    continue

            logger.info(
                "[BEHANCE] Successfully parsed %d projects for user=%s",
                len(projects),
                clean_user,
            )
            return projects

        except Exception as exc:
            raise BehanceScraperError(f"Failed to parse Behance profile page: {exc}")


# Alias for backward compatibility
BehanceScraper = BehanceScraperService
