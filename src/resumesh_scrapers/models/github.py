from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


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
