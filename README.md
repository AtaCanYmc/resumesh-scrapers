# resumesh-scrapers

[![PyPI version](https://img.shields.io/pypi/v/resumesh-scrapers.svg)](https://pypi.org/project/resumesh-scrapers/)
[![Python versions](https://img.shields.io/pypi/pyversions/resumesh-scrapers.svg)](https://pypi.org/project/resumesh-scrapers/)
[![License](https://img.shields.io/pypi/l/resumesh-scrapers.svg)](https://github.com/AtaCanYmc/resumesh-scrapers/blob/main/LICENSE)
[![CI](https://github.com/AtaCanYmc/resumesh-scrapers/actions/workflows/ci.yml/badge.svg)](https://github.com/AtaCanYmc/resumesh-scrapers/actions/workflows/ci.yml)

Standalone, reusable web scraping services for **GitHub**, **Dev.to**, and **Medium** — extracted from the [ResuMesh](https://github.com/AtaCanYmc/ResuMesh) project.

## Installation

```bash
pip install resumesh-scrapers
```

### Development (editable install)

```bash
git clone https://github.com/AtaCanYmc/resumesh-scrapers.git
cd resumesh-scrapers
pip install -e .
```

## Quick Start

```python
import asyncio
from resumesh_scrapers import (
    GitHubScraperService,
    DevToScraperService,
    MediumScraperService,
    ScrapedProject,
    ScrapedArticle,
)

async def main():
    # GitHub
    github = GitHubScraperService()
    projects: list[ScrapedProject] = await github.fetch_data(
        "octocat",
        pat="ghp_...",          # optional — rate limit 60 → 5000/hour
        include_forks=False,    # default
    )
    for p in projects:
        print(f"⭐ {p.stars}  {p.title}")

    # Dev.to
    devto = DevToScraperService()
    articles: list[ScrapedArticle] = await devto.fetch_data(
        "atacanymc",
        api_key="your_key",    # optional
    )

    # Medium
    medium = MediumScraperService()
    articles: list[ScrapedArticle] = await medium.fetch_data("atacanymc")

asyncio.run(main())
```

## Models

| Model | Description |
|---|---|
| `ScrapedProject` | GitHub repository data (title, stars, forks, languages, etc.) |
| `ScrapedArticle` | Blog article data (title, summary, url, platform, etc.) |
| `ArticlePlatform` | Enum: `MEDIUM`, `DEV_TO` |

## Exceptions

All exceptions inherit from `ScraperError`:

- `GitHubScraperError` — GitHub API failures
- `MediumScraperError` — Medium RSS failures
- `DevToScraperError` — Dev.to API failures

```python
from resumesh_scrapers.exceptions import ScraperError

try:
    projects = await scraper.fetch_data("invalid user!")
except ScraperError as e:
    print(f"Scraping failed: {e}")
    print(f"HTTP status: {e.status_code}")  # may be None
```

## ResuMesh Backend Integration

### 1. Install

```bash
pip install resumesh-scrapers
```

### 2. Update imports

```python
# Before (tightly coupled)
from app.services.scrapers.base import IScraperService
from app.services.scrapers.exceptions import ScraperError
from app.services.scrapers.github_scraper import GitHubScraperService

# After (decoupled)
from resumesh_scrapers import GitHubScraperService, IScraperService
from resumesh_scrapers.exceptions import ScraperError
```

### 3. Map scraped data to DB schemas

```python
from resumesh_scrapers import GitHubScraperService, ScrapedProject
from app.schemas.project import ProjectCreate

scraper = GitHubScraperService()
scraped: list[ScrapedProject] = await scraper.fetch_data("octocat")

# Convert to your backend's schema using model_dump()
for project in scraped:
    db_project = ProjectCreate(**project.model_dump())
    await project_repo.upsert_project(db_project)
```

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
