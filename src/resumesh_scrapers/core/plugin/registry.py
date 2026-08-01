"""
Provider Registry & ServiceLoader equivalent for pluggable platform providers.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Optional, Type

if sys.version_info >= (3, 10):
    from importlib.metadata import entry_points
else:
    from importlib_metadata import entry_points

if TYPE_CHECKING:
    from resumesh_scrapers.providers.base import BaseProvider


class ProviderRegistry:
    """
    Central registry for discovering, registering, and instantiating providers.
    Uses Python entry_points ('resumesh.scrapers.providers') for plug-and-play extensions.
    """

    ENTRY_POINT_GROUP = "resumesh.scrapers.providers"

    def __init__(self) -> None:
        self._providers: dict[str, Type[BaseProvider]] = {}
        self._instances: dict[str, BaseProvider] = {}

    def register(self, platform_name: str, provider_cls: Type[BaseProvider]) -> None:
        """Manually register a provider class."""
        self._providers[platform_name.lower()] = provider_cls

    def get_provider_class(self, platform_name: str) -> Optional[Type[BaseProvider]]:
        """Get registered provider class for platform."""
        name = platform_name.lower()
        if name not in self._providers:
            self.discover_plugins()
        return self._providers.get(name)

    def get_provider(self, platform_name: str, **kwargs: Any) -> Optional[BaseProvider]:
        """Get or instantiate provider for platform."""
        name = platform_name.lower()
        if name in self._instances:
            return self._instances[name]

        provider_cls = self.get_provider_class(name)
        if provider_cls is None:
            return None

        instance = provider_cls(**kwargs)
        self._instances[name] = instance
        return instance

    def discover_plugins(self) -> None:
        """Discover external provider plugins registered via entry_points."""
        try:
            if sys.version_info >= (3, 10):
                matched = entry_points(group=self.ENTRY_POINT_GROUP)
            else:
                eps = entry_points()
                matched = eps.get(self.ENTRY_POINT_GROUP, [])  # type: ignore[assignment]

            for ep in matched:
                try:
                    cls = ep.load()
                    name = getattr(cls, "PLATFORM_NAME", ep.name).lower()
                    self._providers[name] = cls
                except Exception:
                    pass
        except Exception:
            pass

    def list_providers(self) -> list[str]:
        """List registered provider names."""
        self.discover_plugins()
        return sorted(list(self._providers.keys()))


# Global default registry instance
registry = ProviderRegistry()
