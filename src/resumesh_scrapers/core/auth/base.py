"""
Abstract CredentialProvider interface for secure authentication token retrieval.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseCredentialProvider(ABC):
    """Abstract CredentialProvider interface."""

    @abstractmethod
    def get_credential(self, platform: str) -> Optional[str]:
        """
        Retrieve API key, OAuth token, or PAT for given platform name.
        """
        pass
