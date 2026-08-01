"""
Static in-memory credential provider.
"""

from typing import Optional

from resumesh_scrapers.core.auth.base import BaseCredentialProvider


class StaticCredentialProvider(BaseCredentialProvider):
    """
    Stores credentials directly in a mapping dictionary.
    """

    def __init__(self, credentials: Optional[dict[str, str]] = None):
        self._credentials = {k.lower(): v for k, v in (credentials or {}).items()}

    def set_credential(self, platform: str, token: str) -> None:
        self._credentials[platform.lower()] = token

    def get_credential(self, platform: str) -> Optional[str]:
        return self._credentials.get(platform.lower())
