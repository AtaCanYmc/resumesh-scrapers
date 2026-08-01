"""
Environment-variable based credential provider.
"""

import os
from typing import Optional
from resumesh_scrapers.core.auth.base import BaseCredentialProvider


class EnvCredentialProvider(BaseCredentialProvider):
    """
    Fetches credentials from environment variables using standardized naming conventions.
    E.g. GITHUB_TOKEN, BEHANCE_API_KEY, DEVTO_API_KEY, MEDIUM_TOKEN.
    """

    PLATFORM_ENV_MAP = {
        "github": ["GITHUB_TOKEN", "GITHUB_PAT", "GH_TOKEN"],
        "behance": ["BEHANCE_API_KEY", "BEHANCE_TOKEN"],
        "devto": ["DEVTO_API_KEY", "DEVTO_TOKEN"],
        "medium": ["MEDIUM_TOKEN", "MEDIUM_API_KEY"],
        "youtube": ["YOUTUBE_API_KEY"],
    }

    def get_credential(self, platform: str) -> Optional[str]:
        keys = self.PLATFORM_ENV_MAP.get(platform.lower(), [f"{platform.upper()}_TOKEN", f"{platform.upper()}_API_KEY"])
        for env_var in keys:
            val = os.getenv(env_var)
            if val:
                return val
        return None
