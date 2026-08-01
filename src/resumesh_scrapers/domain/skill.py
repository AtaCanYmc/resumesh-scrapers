"""
Standardized Skill domain model representing technical skills, languages, or tools.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class Skill(BaseModel):
    """Normalized Skill domain model."""

    platform: str = Field(description="Source platform, e.g. github, npm")
    name: str = Field(description="Name of skill or technology, e.g. Python, React")
    category: Optional[str] = Field(default=None, description="Category, e.g. Language, Framework, Tool")
    level: Optional[str] = Field(default=None, description="Proficiency level if available")
    raw_extra: dict[str, Any] = Field(default_factory=dict, description="Platform specific unmapped payload")
