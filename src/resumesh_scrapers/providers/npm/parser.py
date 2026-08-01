"""
NPM search API response parser.
"""

from typing import Any


class NpmParser:
    """Parses npm registry API search responses."""

    @staticmethod
    def parse_objects(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
        parsed_packages = []
        objects = raw_data.get("objects", [])

        for obj in objects:
            pkg = obj.get("package", {})
            parsed_packages.append(
                {
                    "name": pkg.get("name", ""),
                    "version": pkg.get("version"),
                    "description": pkg.get("description"),
                    "keywords": pkg.get("keywords", []),
                    "links": pkg.get("links", {}),
                    "publisher": pkg.get("publisher", {}),
                    "date": pkg.get("date"),
                    "raw_data": pkg,
                }
            )
        return parsed_packages
