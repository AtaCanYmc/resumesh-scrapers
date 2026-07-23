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


class InfoDownloads(BaseModel):
    last_day: int
    last_month: int
    last_week: int


class Info(BaseModel):
    author: str | None = None
    author_email: str | None = None
    bugtrack_url: str | None = None
    classifiers: list[str] | None = None
    description: str | None = None
    description_content_type: str | None = None
    docs_url: str | None = None
    download_url: str | None = None
    downloads: InfoDownloads
    dynamic: Any | None = None
    home_page: str | None = None
    keywords: str | None = None
    license: str | None = None
    license_expression: str | None = None
    license_files: list[str] | None = None
    maintainer: str | None = None
    maintainer_email: str | None = None
    name: str
    package_url: str | None = None
    platform: str | None = None
    project_url: str | None = None
    project_urls: dict[str, str] | None = None
    provides_extra: list[str] | None = None
    release_url: str | None = None
    requires_dist: list[str] | None = None
    requires_python: str | None = None
    summary: str | None = None
    version: str
    yanked: bool = False
    yanked_reason: str | None = None


class Digests(BaseModel):
    blake2b_256: str
    md5: str
    sha256: str


class ReleaseFile(BaseModel):
    comment_text: str | None = None
    core_metadata: dict | bool | None = Field(default=None, alias="core-metadata")
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str | None = None
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    yanked: bool
    yanked_reason: str | None = None


class Role(BaseModel):
    role: str
    user: str


class Ownership(BaseModel):
    organization: str | None = None
    roles: list[Role]


class PyPiPackageModel(BaseModel):
    info: Info
    last_serial: int
    ownership: Ownership
    releases: dict[str, list[ReleaseFile]]
    urls: list[ReleaseFile]
    vulnerabilities: list[Any] | None = None


class NpmDownloads(BaseModel):
    monthly: int = 0
    weekly: int = 0


class NpmUser(BaseModel):
    username: str | None = None
    email: str | None = None


class NpmLinks(BaseModel):
    npm: str | None = None
    homepage: str | None = None
    repository: str | None = None
    bugs: str | None = None


class NpmPackage(BaseModel):
    name: str
    version: str
    description: str | None = None
    keywords: list[str] | None = None
    sanitized_name: str | None = None
    publisher: NpmUser | None = None
    maintainers: list[NpmUser] = Field(default_factory=list)
    license: str | None = None
    date: str | None = None
    links: NpmLinks | None = None


class NpmScoreDetail(BaseModel):
    popularity: float = 0.0
    quality: float = 0.0
    maintenance: float = 0.0


class NpmScore(BaseModel):
    final: float = 0.0
    detail: NpmScoreDetail | None = None


class NpmFlags(BaseModel):
    insecure: int | None = None
    unstable: bool | None = None
    deprecated: str | bool | None = None


class NpmSearchObject(BaseModel):
    package: NpmPackage
    downloads: NpmDownloads | None = None
    dependents: int = 0
    updated: str | None = None
    searchScore: float = Field(default=0.0, alias="searchScore")
    score: NpmScore | None = None
    flags: NpmFlags | dict[str, Any] | None = None


class NpmSearchResultModel(BaseModel):
    objects: list[NpmSearchObject] = Field(default_factory=list)
    total: int = 0
    time: str | None = None
