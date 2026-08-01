"""
PyPI JSON API and HTML profile parser.
"""

from typing import Any

from bs4 import BeautifulSoup


class PyPiParser:
    """Parses PyPI JSON API responses and profile HTML."""

    @staticmethod
    def parse_profile_packages(html_content: str) -> list[str]:
        soup = BeautifulSoup(html_content, "html.parser")
        return [h3.text.strip() for h3 in soup.find_all("h3", class_="package-snippet__title")]

    @staticmethod
    def parse_package(raw_data: dict[str, Any]) -> dict[str, Any]:
        info = raw_data.get("info", {})
        return {
            "name": info.get("name", ""),
            "version": info.get("version"),
            "summary": info.get("summary"),
            "home_page": info.get("home_page") or info.get("package_url"),
            "package_url": info.get("package_url"),
            "author": info.get("author"),
            "license": info.get("license"),
            "keywords": info.get("keywords"),
            "raw_data": raw_data,
        }
