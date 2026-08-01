"""
Standardized Experience domain model representing work, open source, or project experiences.
"""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class Experience(BaseModel):
    """Normalized Experience domain model."""

    platform: str = Field(description="Platform name, e.g. github, linkedin")
    role: str = Field(description="Job title, contribution role, or position")
    organization: Optional[str] = Field(default=None, description="Company, organization, or project name")
    location: Optional[str] = Field(default=None, description="Location of work")
    start_date: Optional[datetime] = Field(default=None, description="Start date")
    end_date: Optional[datetime] = Field(default=None, description="End date (None if current)")
    description: Optional[str] = Field(default=None, description="Detailed responsibilities or achievements")
    skills: list[str] = Field(default_factory=list, description="Technologies or skills used")
    raw_extra: dict[str, Any] = Field(default_factory=dict, description="Platform specific unmapped payload")
