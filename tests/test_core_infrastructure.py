"""
Unit tests for Core layer infrastructure (Cache, RateLimiter, Auth, Registry).
"""

import pytest
from resumesh_scrapers.core import (
    EnvCredentialProvider,
    InMemoryCache,
    ProviderRegistry,
    RateLimiter,
    StaticCredentialProvider,
    registry,
)
from resumesh_scrapers.providers import GitHubProvider


@pytest.mark.asyncio
async def test_in_memory_cache():
    cache = InMemoryCache(default_ttl_seconds=10)
    await cache.set("key1", "value1")
    val = await cache.get("key1")
    assert val == "value1"

    await cache.delete("key1")
    assert await cache.get("key1") is None


@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(requests_per_second=100.0, delay_seconds=0.0)

    async def sample():
        return 42

    res = await limiter.execute_with_retry(sample)
    assert res == 42


def test_credential_providers(monkeypatch):
    static_auth = StaticCredentialProvider({"github": "secret_token"})
    assert static_auth.get_credential("github") == "secret_token"
    assert static_auth.get_credential("devto") is None

    monkeypatch.setenv("GITHUB_TOKEN", "env_github_token")
    env_auth = EnvCredentialProvider()
    assert env_auth.get_credential("github") == "env_github_token"


def test_provider_registry():
    reg = ProviderRegistry()
    reg.register("github", GitHubProvider)

    assert "github" in reg.list_providers()
    provider_cls = reg.get_provider_class("github")
    assert provider_cls == GitHubProvider

    instance = reg.get_provider("github")
    assert isinstance(instance, GitHubProvider)


def test_global_registry():
    providers = registry.list_providers()
    assert "github" in providers
    assert "devto" in providers
    assert "medium" in providers
    assert "substack" in providers
    assert "behance" in providers
    assert "npm" in providers
    assert "pypi" in providers
    assert "youtube" in providers
