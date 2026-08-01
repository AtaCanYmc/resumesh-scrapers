<p align="center">
  <img src="https://raw.githubusercontent.com/AtaCanYmc/resumesh-scrapers/main/assets/banner.png" alt="ResuMesh Scrapers Banner" width="600" style="max-width: 100%;" onerror="this.style.display='none'" />
</p>

<h1 align="center">resumesh-scrapers</h1>

<p align="center">
  <strong>A pluggable Python framework that collects, normalizes, and synchronizes developer profile data from multiple platforms into unified domain models.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/resumesh-scrapers/"><img src="https://img.shields.io/pypi/v/resumesh-scrapers.svg" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/resumesh-scrapers/"><img src="https://img.shields.io/pypi/pyversions/resumesh-scrapers.svg" alt="Python versions" /></a>
  <a href="https://github.com/AtaCanYmc/resumesh-scrapers/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/resumesh-scrapers.svg" alt="License" /></a>
  <a href="https://github.com/AtaCanYmc/resumesh-scrapers/actions/workflows/ci.yml"><img src="https://github.com/AtaCanYmc/resumesh-scrapers/actions/workflows/ci.yml/badge.svg" alt="CI Status" /></a>
</p>

---

`resumesh-scrapers` is an enterprise-grade, pluggable developer data integration framework supporting **GitHub**, **Dev.to**, **Medium**, **Substack**, **Behance**, **NPM**, **PyPI**, and **YouTube**.

Rather than returning raw, platform-specific payloads, `resumesh-scrapers` normalizes all data into unified domain entities: **`Profile`**, **`Project`**, **`Article`**, **`Video`**, **`Experience`**, and **`Skill`**.

---

## 🚀 Key Features

*   **Pluggable Provider Architecture:** Implement custom providers or discover community plugins dynamically via Python entry points (`resumesh.scrapers.providers`).
*   **Normalized Domain Models:** Unified `Profile`, `Project`, `Article`, `Video`, `Experience`, and `Skill` models across all platforms.
*   **Decoupled HTTP & Resilience:** Abstracted HTTP client (`BaseHttpClient`) with built-in rate limiting, delay, backoff, and random jitter.
*   **In-Memory & TTL Caching:** `InMemoryCache` with TTL support to prevent unnecessary HTTP requests.
*   **Parser & Mapper Separation:** Clean single-responsibility separation between raw extraction (`Parser`) and domain transformation (`Mapper`).
*   **CredentialProvider System:** Secure token & API key retrieval from environment variables (`EnvCredentialProvider`) or static configuration.
*   **Structured Exception Hierarchy:** Standardized exceptions (`ScraperError`, `RateLimitError`, `AuthenticationError`, `ParsingError`, `NetworkError`).

---

## 📊 Capability Matrix

| Platform | Provider Class | `Profile` | `Project` | `Article` | `Video` | Primary Data Source |
|---|---|:---:|:---:|:---:|:---:|---|
| **GitHub** | `GitHubProvider` | ✅ | ✅ | ❌ | ❌ | REST API (v3) |
| **Dev.to** | `DevToProvider` | ✅ | ❌ | ✅ | ❌ | REST API (Forem v1) |
| **Medium** | `MediumProvider` | ✅ | ❌ | ✅ | ❌ | RSS Feed |
| **Substack** | `SubstackProvider` | ✅ | ❌ | ✅ | ❌ | RSS Feed |
| **Behance** | `BehanceProvider` | ✅ | ✅ | ❌ | ❌ | REST API (v2) / HTML Scraping |
| **NPM** | `NpmProvider` | ✅ | ✅ | ❌ | ❌ | Registry Search API |
| **PyPI** | `PyPiProvider` | ✅ | ✅ | ❌ | ❌ | JSON API & User HTML |
| **YouTube** | `YouTubeProvider` | ✅ | ❌ | ❌ | ✅ | `yt-dlp` Extraction |

---

## 🛠️ Installation

```bash
pip install resumesh-scrapers
```

### For Local Development (Editable mode)

```bash
git clone https://github.com/AtaCanYmc/resumesh-scrapers.git
cd resumesh-scrapers
pip install -e .
```

---

## 💡 Quick Start (Provider API)

```python
import asyncio
from resumesh_scrapers import registry, Profile, Project, Article, Video

async def main():
    # 1. Access Provider Registry
    github_provider = registry.get_provider("github")

    # 2. Get Normalized Profile
    profile: Profile = await github_provider.get_profile("octocat")
    print(f"Profile: {profile.name} (@{profile.username}) - {profile.website}")

    # 3. Get Normalized Projects
    projects: list[Project] = await github_provider.get_projects("octocat")
    print(f"Fetched {len(projects)} normalized projects.")

    # 4. Get Normalized Articles (Dev.to / Medium)
    devto_provider = registry.get_provider("devto")
    articles: list[Article] = await devto_provider.get_articles("atacanymc")
    print(f"Fetched {len(articles)} articles.")

    # 5. Get Normalized Videos (YouTube)
    youtube_provider = registry.get_provider("youtube")
    videos: list[Video] = await youtube_provider.get_videos("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Video: {videos[0].title} ({videos[0].duration_seconds}s)")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🗺️ Architecture Overview

```text
src/resumesh_scrapers/
├── domain/                     # Unified domain entities (Profile, Project, Article, Video, Experience, Skill)
├── core/
│   ├── http/                   # BaseHttpClient & HttpxHttpClient
│   ├── resilience/             # RateLimiter (Backoff, Delay, Jitter)
│   ├── cache/                  # InMemoryCache (TTL)
│   ├── auth/                   # CredentialProvider (Env & Static)
│   └── plugin/                 # ProviderRegistry & Entry Points discovery
├── providers/                  # Pluggable platform implementations
│   ├── base.py                 # BaseProvider contract
│   ├── github/                 # GitHubProvider, GitHubParser, GitHubMapper
│   ├── devto/                  # DevToProvider, DevToParser, DevToMapper
│   ├── medium/                 # MediumProvider, MediumParser, MediumMapper
│   ├── substack/               # SubstackProvider, SubstackParser, SubstackMapper
│   ├── behance/                # BehanceProvider, BehanceParser, BehanceMapper
│   ├── npm/                    # NpmProvider, NpmParser, NpmMapper
│   ├── pypi/                   # PyPiProvider, PyPiParser, PyPiMapper
│   └── youtube/                # YouTubeProvider, YouTubeParser, YouTubeMapper
└── exceptions.py               # Structured exception hierarchy
```

---

## 📄 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.
