"""
Substack Provider package.
"""

from resumesh_scrapers.providers.substack.mapper import SubstackMapper
from resumesh_scrapers.providers.substack.parser import SubstackParser
from resumesh_scrapers.providers.substack.provider import SubstackProvider

__all__ = ["SubstackProvider", "SubstackParser", "SubstackMapper"]
