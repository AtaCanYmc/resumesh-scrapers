"""
Behance API and HTML profile parser.
"""

import re
from typing import Any

from bs4 import BeautifulSoup


class BehanceParser:
    """Parses Behance API JSON payloads and HTML profile pages."""

    @staticmethod
    def parse_api_projects(raw_projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
        parsed: list[dict[str, Any]] = []
        for proj in raw_projects:
            covers = proj.get("covers", {})
            covers_url = covers.get("original") or covers.get("max_808") or covers.get("404")
            parsed.append(
                {
                    "id": str(proj.get("id")) if proj.get("id") else None,
                    "name": proj.get("name", "Untitled Project"),
                    "url": proj.get("url"),
                    "published_on": proj.get("published_on"),
                    "appreciations": proj.get("stats", {}).get("appreciations", 0),
                    "views": proj.get("stats", {}).get("views", 0),
                    "covers_url": covers_url,
                    "tags": proj.get("fields", []),
                    "raw_data": proj,
                }
            )
        return parsed

    @staticmethod
    def parse_html_projects(html_content: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html_content, "html.parser")
        parsed: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        project_cards = soup.select("div.project-card, [class*='ProjectCover']")
        for card in project_cards:
            title_elem = card.select_one("a.projekt-link, [class*='Title'], [class*='title'], h3")
            title = title_elem.get_text(strip=True) if title_elem else "Untitled Project"

            link_elem = card.select_one("a[href*='/gallery/']")
            href = link_elem.get("href") if link_elem else None
            project_url = str(href) if href else None
            if project_url and not project_url.startswith("http"):
                project_url = f"https://www.behance.net{project_url}"

            if not project_url or project_url in seen_urls:
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

            parsed.append(
                {
                    "name": title,
                    "url": project_url,
                    "appreciations": appreciations,
                    "raw_data": {},
                }
            )
        return parsed
