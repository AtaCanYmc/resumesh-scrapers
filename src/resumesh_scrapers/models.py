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
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: GitHubOwner
    html_url: HttpUrl
    description: Optional[str] = None
    fork: bool
    url: HttpUrl
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    homepage: Optional[HttpUrl | str] = None
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str] = None
    forks_count: int
    open_issues_count: int
    license: Optional[GitHubLicense] = None
    topics: list[str] = Field(default_factory=list)
    visibility: str
    default_branch: str
    # config
    model_config = ConfigDict(extra="ignore")
