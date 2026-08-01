"""
02_advanced_provider_configuration.py
======================================
Enterprise example showing custom RateLimiter, InMemoryCache TTL tuning,
StaticCredentialProvider token injection, and custom HttpxHttpClient setup.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from resumesh_scrapers import (
    GitHubProvider,
    HttpxHttpClient,
    InMemoryCache,
    Profile,
    Project,
    RateLimiter,
    StaticCredentialProvider,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("=== 02. Advanced Provider Configuration Demo ===")

    # 1. Custom HTTP Client with custom User-Agent and timeout
    custom_http = HttpxHttpClient(
        headers={"User-Agent": "Enterprise-Portfolio-Bot/2.0 (+https://example.com)"},
        timeout=25.0,
    )

    # 2. Custom Cache with 1-hour TTL
    custom_cache = InMemoryCache(default_ttl_seconds=3600)

    # 3. Custom Rate Limiter with delay & backoff settings
    custom_limiter = RateLimiter(
        requests_per_second=2.0,
        delay_seconds=0.5,
        jitter=True,
        max_retries=5,
    )

    # 4. Custom Credential Provider with in-memory API tokens
    custom_auth = StaticCredentialProvider(
        credentials={
            "github": "ghp_mock_token_for_higher_rate_limits",
            "behance": "behance_mock_api_key",
        }
    )

    # 5. Instantiate GitHubProvider with injected enterprise dependencies
    provider = GitHubProvider(
        http_client=custom_http,
        cache=custom_cache,
        rate_limiter=custom_limiter,
        credential_provider=custom_auth,
    )

    logger.info("Initialized GitHubProvider with custom enterprise pipeline components.")

    # 6. Perform cached & rate-limited requests
    profile: Optional[Profile] = await provider.get_profile("octocat")
    if profile:
        logger.info("Fetched Profile: %s", profile.name)

    # Second call uses cache instantaneously
    cached_profile: Optional[Profile] = await provider.get_profile("octocat")
    logger.info("Second fetch retrieved from cache: %s", cached_profile is not None)

    projects: list[Project] = await provider.get_projects("octocat")
    logger.info("Fetched %d projects.", len(projects))

    # Clean up HTTP sessions
    await custom_http.close()


if __name__ == "__main__":
    asyncio.run(main())
