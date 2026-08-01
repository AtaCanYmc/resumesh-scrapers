"""
BaseProvider interface enforcing uniform scraping and data collection contracts.
"""

from abc import ABC, abstractmethod
from typing import Optional
from resumesh_scrapers.core.auth import BaseCredentialProvider, EnvCredentialProvider
from resumesh_scrapers.core.cache import BaseCache, InMemoryCache
from resumesh_scrapers.core.http import BaseHttpClient, HttpxHttpClient
from resumesh_scrapers.core.resilience import RateLimiter
from resumesh_scrapers.domain import Article, Experience, Profile, Project, Skill, Video


class BaseProvider(ABC):
    """
    Abstract Base Class for platform providers.
    Normalizes platform data extraction into unified domain models.
    """

    PLATFORM_NAME: str = "base"

    def __init__(
        self,
        http_client: Optional[BaseHttpClient] = None,
        cache: Optional[BaseCache] = None,
        rate_limiter: Optional[RateLimiter] = None,
        credential_provider: Optional[BaseCredentialProvider] = None,
    ):
        self.http_client = http_client or HttpxHttpClient()
        self.cache = cache or InMemoryCache()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.credential_provider = credential_provider or EnvCredentialProvider()

    @abstractmethod
    async def get_profile(self, identifier: str) -> Optional[Profile]:
        """Fetch and normalize user profile."""
        pass

    @abstractmethod
    async def get_projects(self, identifier: str) -> list[Project]:
        """Fetch and normalize projects / repositories."""
        pass

    @abstractmethod
    async def get_articles(self, identifier: str) -> list[Article]:
        """Fetch and normalize articles / posts / publications."""
        pass

    async def get_videos(self, identifier: str) -> list[Video]:
        """Fetch and normalize video content across video platforms."""
        return []

    async def get_publications(self, identifier: str) -> list[Article]:
        """Alias for get_articles() to retrieve written articles or newsletters."""
        return await self.get_articles(identifier)

    async def get_experiences(self, identifier: str) -> list[Experience]:
        """Fetch and normalize work / contribution experiences."""
        return []

    async def get_skills(self, identifier: str) -> list[Skill]:
        """Fetch and normalize user skills / languages."""
        return []
