"""
Standardized Profile domain model representing developer profile details across platforms.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class Profile(BaseModel):
    """Normalized Profile domain model."""

    platform: str = Field(description="Platform name, e.g. github, medium, devto")
    username: str = Field(description="User identifier on the platform")
    name: Optional[str] = Field(default=None, description="Full name or display name")
    bio: Optional[str] = Field(default=None, description="Short bio or tagline")
    avatar_url: Optional[str] = Field(default=None, description="Avatar or profile picture URL")
    location: Optional[str] = Field(default=None, description="User location")
    company: Optional[str] = Field(default=None, description="User organization or company")
    website: Optional[str] = Field(default=None, description="Personal website or primary blog URL")
    social_links: dict[str, str] = Field(default_factory=dict, description="Social media/external links")
    raw_extra: dict[str, Any] = Field(default_factory=dict, description="Platform specific unmapped payload")
