"""
Package-own Pydantic models for scraped data.

These models are **completely independent** of the FastAPI backend's
database models and schemas. Consumers of this package should map
these models to their own domain objects.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class ArticlePlatform(str, Enum):
    """Supported article platforms."""

    MEDIUM = "MEDIUM"
    DEV_TO = "DEV_TO"


class ScrapedProject(BaseModel):
    """
    Generic representation of a scraped project/repository.

    Maps 1-to-1 with the fields previously found in
    ``app.schemas.project.ProjectCreate`` but carries no
    FastAPI or SQLAlchemy dependency.
    """

    title: str
    description: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    stars: int = 0
    watchers: int = 0
    forks: int = 0
    languages: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    raw_github_data: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


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
