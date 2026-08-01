"""
Standardized Video domain model representing video content, tutorials, or streams across platforms.
"""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class Video(BaseModel):
    """Normalized Video domain model."""

    platform: str = Field(description="Platform name, e.g. youtube, vimeo, twitch")
    title: str = Field(description="Video title")
    url: str = Field(description="Canonical video URL")
    description: Optional[str] = Field(default=None, description="Video description or summary")
    duration_seconds: Optional[int] = Field(default=None, description="Video duration in seconds")
    published_at: Optional[datetime] = Field(default=None, description="Publication timestamp")
    view_count: Optional[int] = Field(default=0, description="Total views count")
    like_count: Optional[int] = Field(default=0, description="Total likes count")
    thumbnail_url: Optional[str] = Field(default=None, description="Thumbnail image URL")
    tags: list[str] = Field(default_factory=list, description="Categories or tags")
    raw_extra: dict[str, Any] = Field(default_factory=dict, description="Platform specific unmapped payload")
