"""
Authentication and credential provider abstractions.
"""

from resumesh_scrapers.core.auth.base import BaseCredentialProvider
from resumesh_scrapers.core.auth.env import EnvCredentialProvider
from resumesh_scrapers.core.auth.static import StaticCredentialProvider

__all__ = [
    "BaseCredentialProvider",
    "EnvCredentialProvider",
    "StaticCredentialProvider",
]
