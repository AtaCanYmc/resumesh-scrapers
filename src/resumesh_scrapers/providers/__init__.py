"""
Platform data providers and base contract.
"""

from resumesh_scrapers.core.plugin import registry
from resumesh_scrapers.providers.base import BaseProvider
from resumesh_scrapers.providers.behance import BehanceProvider
from resumesh_scrapers.providers.devto import DevToProvider
from resumesh_scrapers.providers.github import GitHubProvider
from resumesh_scrapers.providers.medium import MediumProvider
from resumesh_scrapers.providers.npm import NpmProvider
from resumesh_scrapers.providers.pypi import PyPiProvider
from resumesh_scrapers.providers.substack import SubstackProvider
from resumesh_scrapers.providers.youtube import YouTubeProvider

# Register default built-in providers
registry.register("github", GitHubProvider)
registry.register("devto", DevToProvider)
registry.register("medium", MediumProvider)
registry.register("substack", SubstackProvider)
registry.register("behance", BehanceProvider)
registry.register("npm", NpmProvider)
registry.register("pypi", PyPiProvider)
registry.register("youtube", YouTubeProvider)

__all__ = [
    "BaseProvider",
    "GitHubProvider",
    "DevToProvider",
    "MediumProvider",
    "SubstackProvider",
    "BehanceProvider",
    "NpmProvider",
    "PyPiProvider",
    "YouTubeProvider",
]
