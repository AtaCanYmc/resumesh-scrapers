<p align="center">
  <img src="https://raw.githubusercontent.com/AtaCanYmc/resumesh-scrapers/main/assets/banner.png" alt="ResuMesh Scrapers Banner" width="600" style="max-width: 100%;" onerror="this.style.display='none'" />
</p>

<h1 align="center">resumesh-scrapers</h1>

<p align="center">
  <strong>Enterprise-Grade, Standalone, and Decoupled Web Scraping Engines for Portfolio Building</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/resumesh-scrapers/"><img src="https://img.shields.io/pypi/v/resumesh-scrapers.svg" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/resumesh-scrapers/"><img src="https://img.shields.io/pypi/pyversions/resumesh-scrapers.svg" alt="Python versions" /></a>
  <a href="https://github.com/AtaCanYmc/resumesh-scrapers/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/resumesh-scrapers.svg" alt="License" /></a>
  <a href="https://github.com/AtaCanYmc/resumesh-scrapers/actions/workflows/ci.yml"><img src="https://github.com/AtaCanYmc/resumesh-scrapers/actions/workflows/ci.yml/badge.svg" alt="CI Status" /></a>
</p>

---

`resumesh-scrapers` is a clean, modular, and robust Python library containing standalone scraping services for **GitHub**, **Dev.to**, **Medium**, **Substack**, **Behance**, **NPM**, and **PyPI** platforms. Originally developed as part of the [ResuMesh](https://github.com/AtaCanYmc/ResuMesh) ecosystem, it has been decoupled to serve as a reusable package for any resume, portfolio, or profile aggregator project.

## 🚀 Key Features

*   **Robust Core Network Engine:** Centralized HTTP request handling with standard retry mechanisms powered by `tenacity` and structured logging.
*   **Fully Decoupled Models:** Independent, clean data validation using `pydantic` v2, keeping data structures separated from database constraints.
*   **Extensible Architecture:** Platform scrapers are isolated in a plug-and-play layout under `platforms/` allowing quick addition of new integrations (e.g. LinkedIn, GitLab).
*   **Detailed Exceptions:** Standardized exceptions hierarchy inheriting from `ScraperError` with HTTP status code details.

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

## 💡 Quick Start

Here is a simple example showing how to scrape your repository and blog statistics:

```python
import asyncio
from resumesh_scrapers import (
    GitHubScraper,
    DevToScraper,
    MediumScraper,
    SubstackScraper,
    BehanceScraper,
    GitHubRepositoryModel,
    ScrapedArticle,
    BehanceProjectModel,
)

async def main():
    # 1. Scraping GitHub Repositories
    github = GitHubScraper()
    repos: list[GitHubRepositoryModel] = await github.fetch_data(
        username="octocat",
        pat="ghp_...",  # optional PAT token to bypass rate limit
        include_forks=False
    )
    print(f"Fetched {len(repos)} repositories.")

    # 2. Scraping Dev.to Articles
    devto = DevToScraper()
    devto_posts: list[ScrapedArticle] = await devto.fetch_data("atacanymc")
    print(f"Fetched {len(devto_posts)} Dev.to articles.")

    # 3. Scraping Substack Publications
    substack = SubstackScraper()
    substack_posts: list[ScrapedArticle] = await substack.fetch_data("atacan")
    print(f"Fetched {len(substack_posts)} Substack posts.")

    # 4. Scraping Behance Projects
    behance = BehanceScraper()
    behance_projects: list[BehanceProjectModel] = await behance.fetch_data("atacanymc")
    print(f"Fetched {len(behance_projects)} Behance projects.")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🗺️ Clean Architecture

The codebase has been refactored to enforce separation of concerns, decoupling models, platforms, and network layers:

```text
src/resumesh_scrapers/
├── core/                       # Shared network and utility systems
│   ├── client.py               # Central HTTP requester with tenacity retries
│   └── __init__.py
├── platforms/                  # Individual platform scrapers
│   ├── github.py
│   ├── devto.py
│   ├── medium.py
│   ├── substack.py
│   ├── behance.py
│   ├── npm.py
│   ├── pypi.py
│   └── __init__.py
└── models/                     # Platform-specific Pydantic validation schemas
    ├── github.py
    ├── article.py              # Dev.to, Medium, Substack shared schemas
    ├── behance.py
    ├── npm.py
    ├── pypi.py
    └── __init__.py
```

---

## 📊 Models & Capabilities

| Platform | Scraper Class | Response Model | Captured Data Features |
|---|---|---|---|
| **GitHub** | `GitHubScraper` | `GitHubRepositoryModel` | Stars, Forks, Main languages, Visibility, Watchers, Creation dates |
| **Dev.to** | `DevToScraper` | `ScrapedArticle` | Title, URL, Tags, Reading time, Publishing date |
| **Medium** | `MediumScraper` | `ScrapedArticle` | Title, RSS Summary, UTM-stripped URL, Category tags |
| **Substack** | `SubstackScraper` | `ScrapedArticle` | Title, RSS Summary, URL, Reading time estimation |
| **Behance** | `BehanceScraper` | `BehanceProjectModel` | Project title, gallery URL, appreciation count, publication dates |
| **NPM** | `NpmScraper` | `NpmSearchResultModel` | Maintainer packages, keywords, version history, publisher metadata |
| **PyPI** | `PyPIScraper` | `PyPiPackageModel` | Releases, download statistics, license, project metadata |

---

## ⚠️ Exception Handling

All scraper exceptions inherit from `ScraperError` to simplify integration errors:

```python
from resumesh_scrapers.exceptions import ScraperError, GitHubScraperError

try:
    repos = await github_scraper.fetch_data("some_username")
except GitHubScraperError as e:
    print(f"GitHub API Error: {e.message} (HTTP {e.status_code})")
except ScraperError as e:
    print(f"Generic Scraping Exception: {e}")
```

---

## 🤝 Contributing

We welcome contributions to add more platforms (such as LinkedIn, GitLab, or Dribbble) or optimize parsers. Please open a Pull Request or file an issue to discuss your ideas!

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.
