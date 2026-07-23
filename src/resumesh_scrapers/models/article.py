from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, HttpUrl


class ArticlePlatform(str, Enum):
    """Supported article platforms."""

    MEDIUM = "MEDIUM"
    DEV_TO = "DEV_TO"
    SUBSTACK = "SUBSTACK"


class ScrapedArticle(BaseModel):
    """
    Generic representation of a scraped article/blog post.

    Maps 1-to-1 with the fields previously found in
    ``app.schemas.article.ArticleCreate`` but carries no
    FastAPI or SQLAlchemy dependency.
    """

    title: str
    summary: Optional[str] = None
    url: HttpUrl
    platform: ArticlePlatform
    reading_time_minutes: int = 0
    published_at: Optional[datetime] = None
    raw_platform_data: Optional[Dict[str, Any]] = None
