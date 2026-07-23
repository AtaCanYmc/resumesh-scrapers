from abc import ABC, abstractmethod
from typing import Any, List


class IScraperService(ABC):
    """
    Base interface for all platform scrapers.
    Enforces the Open/Closed Principle and Dependency Inversion.
    """

    @abstractmethod
    async def fetch_data(self, username: str, **kwargs) -> List[Any]:
        """
        Fetches data from the platform.

        Args:
            username: The username or identifier on the platform.
            **kwargs: Additional optional parameters (e.g., tokens, filters).

        Returns:
            A list of parsed Pydantic model objects
            (e.g., ScrapedProject, ScrapedArticle).
        """
        pass
