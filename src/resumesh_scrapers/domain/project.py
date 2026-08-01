"""
Standardized Project domain model representing repositories, software packages, or portfolio projects.
"""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class Project(BaseModel):
    """Normalized Project domain model."""

    platform: str = Field(description="Platform name, e.g. github, npm, pypi, behance")
    name: str = Field(description="Project or repository name")
    description: Optional[str] = Field(default=None, description="Summary or description of the project")
    url: str = Field(description="Canonical HTTP URL to the project")
    stars: int = Field(default=0, description="Star count, appreciations, or likes")
    forks: int = Field(default=0, description="Fork count")
    language: Optional[str] = Field(default=None, description="Primary programming language or category")
    topics: list[str] = Field(default_factory=list, description="Tags, keywords, or topics")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last updated timestamp")
    raw_extra: dict[str, Any] = Field(default_factory=dict, description="Platform specific unmapped payload")
