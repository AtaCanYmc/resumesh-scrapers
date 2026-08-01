"""
Standardized Article / Publication domain model representing blog posts, articles, videos, podcast episodes, or newsletter publications.
"""

from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class Article(BaseModel):
    """Normalized Article / Publication domain model."""

    platform: str = Field(description="Platform name, e.g. devto, medium, substack, youtube")
    content_type: str = Field(default="article", description="Type of content: article, video, podcast, presentation")
    title: str = Field(description="Content title")
    url: str = Field(description="Canonical URL of the content")
    summary: Optional[str] = Field(default=None, description="Short snippet, abstract, or description")
    content: Optional[str] = Field(default=None, description="Full body content if extracted")
    published_at: Optional[datetime] = Field(default=None, description="Publication timestamp")
    tags: list[str] = Field(default_factory=list, description="Categories, tags, or topics")
    reading_time_minutes: Optional[int] = Field(default=None, description="Estimated reading or watching time in minutes")
    raw_extra: dict[str, Any] = Field(default_factory=dict, description="Platform specific unmapped payload")


# Alias for generalized content model naming
Publication = Article
ContentItem = Article
