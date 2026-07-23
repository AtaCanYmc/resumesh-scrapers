"""
Package-own Pydantic models for scraped data.

These models are **completely independent** of the FastAPI backend's
database models and schemas. Consumers of this package should map
these models to their own domain objects.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


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


class GitHubOwner(BaseModel):
    """Represents the owner details of a GitHub repository."""
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    html_url: HttpUrl
    type: str
    site_admin: bool


class GitHubLicense(BaseModel):
    """Represents repository license information."""
    key: str
    name: str
    spdx_id: Optional[str] = None
    url: Optional[HttpUrl] = None


class GitHubRepositoryModel(BaseModel):
    """Pydantic model for raw repository data fetched by the GitHub scraper."""
    id: Optional[int] = None
    node_id: Optional[str] = None
    name: str
    full_name: Optional[str] = None
    private: bool = False
    owner: Optional[GitHubOwner] = None
    html_url: Optional[HttpUrl | str] = None
    description: Optional[str] = None
    fork: bool = False
    url: Optional[HttpUrl | str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pushed_at: Optional[datetime] = None
    homepage: Optional[HttpUrl | str] = None
    size: int = 0
    stargazers_count: int = Field(default=0, validation_alias="stars")
    watchers_count: int = 0
    forks_count: int = 0
    language: Optional[str] = None
    languages: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    open_issues_count: int = 0
    license: Optional[GitHubLicense] = None
    visibility: str = "public"
    default_branch: str = "main"

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class BehanceProjectModel(BaseModel):
    """Pydantic model for raw project data fetched or parsed from Behance."""
    id: Optional[str] = None
    name: str
    url: HttpUrl
    published_on: Optional[datetime] = None
    stats_appreciations: int = 0
    stats_views: int = 0
    covers_url: Optional[HttpUrl | str] = None
    tags: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")
