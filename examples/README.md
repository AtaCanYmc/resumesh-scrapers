# ResuMesh Scrapers - Enterprise Reference Examples

This directory provides enterprise-grade, production-ready reference implementations for `resumesh-scrapers`.

---

## 📂 Suite Overview

| File | Level | Description |
|---|---|---|
| [`01_basic_usage.py`](01_basic_usage.py) | **Beginner** | Basic profile, project, article, and video retrieval via `registry` and normalized domain models. |
| [`02_advanced_provider_configuration.py`](02_advanced_provider_configuration.py) | **Intermediate** | Custom `RateLimiter` backoff, `InMemoryCache` TTL tuning, `StaticCredentialProvider`, and custom `HttpxHttpClient`. |
| [`03_custom_provider_plugin.py`](03_custom_provider_plugin.py) | **Advanced** | Creating a 3rd party provider (`KaggleProvider`), parser, and mapper, and registering it dynamically into `ProviderRegistry`. |
| [`04_developer_profile_aggregator.py`](04_developer_profile_aggregator.py) | **Enterprise** | Concurrent multi-platform portfolio sync script across 8 platforms into a unified JSON resume payload. |
| [`05_legacy_compatibility.py`](05_legacy_compatibility.py) | **Migration** | Demonstrating backward compatibility for legacy scraper services (`GitHubScraper`, `DevToScraper`, etc.). |

---

## 🚀 How to Run Examples

Activate your virtual environment and execute any script directly with python:

```bash
# 1. Basic Usage Demo
python examples/01_basic_usage.py

# 2. Advanced Enterprise Provider Configuration
python examples/02_advanced_provider_configuration.py

# 3. Custom Third-Party Provider Plugin (Kaggle Example)
python examples/03_custom_provider_plugin.py

# 4. Multi-Platform Developer Profile Aggregator
python examples/04_developer_profile_aggregator.py

# 5. Legacy Compatibility Scrapers
python examples/05_legacy_compatibility.py
```

---

## 🔑 Authentication Credentials (Optional)

You can set environment variables for platforms requiring API tokens to bypass rate limits:

```bash
export GITHUB_TOKEN="ghp_your_personal_access_token"
export DEVTO_API_KEY="your_devto_api_key"
export BEHANCE_API_KEY="your_behance_api_key"
```

The `EnvCredentialProvider` automatically detects these variables at runtime!
