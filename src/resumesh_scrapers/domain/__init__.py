"""
Standardized domain models for unified developer profile data integration.
"""

from resumesh_scrapers.domain.article import Article, ContentItem, Publication
from resumesh_scrapers.domain.experience import Experience
from resumesh_scrapers.domain.profile import Profile
from resumesh_scrapers.domain.project import Project
from resumesh_scrapers.domain.skill import Skill
from resumesh_scrapers.domain.video import Video

__all__ = [
    "Profile",
    "Project",
    "Article",
    "Publication",
    "ContentItem",
    "Video",
    "Experience",
    "Skill",
]
