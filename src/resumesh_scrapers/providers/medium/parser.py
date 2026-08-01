"""
Medium RSS feed parser.
"""

import html
import re
from typing import Any

import feedparser


class MediumParser:
    """Parses Medium RSS feed XML using feedparser."""

    @staticmethod
    def parse_feed(raw_xml: str) -> list[dict[str, Any]]:
        feed = feedparser.parse(raw_xml)
        parsed_entries = []

        for entry in feed.entries:
            clean_url = entry.get("link", "").split("?")[0]
            raw_summary = entry.get("summary", "") or ""
            clean_summary = re.sub(r"<[^>]+>", "", raw_summary).strip()
            clean_summary = html.unescape(clean_summary)

            tags = [t.term for t in entry.get("tags", []) if getattr(t, "term", None)]

            parsed_entries.append(
                {
                    "title": entry.get("title", ""),
                    "url": clean_url,
                    "summary": clean_summary,
                    "published_at": entry.get("published"),
                    "tags": tags,
                    "raw_data": dict(entry),
                }
            )
        return parsed_entries
