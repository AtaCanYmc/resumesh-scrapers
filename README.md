# resumesh-scrapers

Standalone, reusable web scraping services for **GitHub**, **Dev.to**, and **Medium** — extracted from the [ResuMesh](https://github.com/AtaCanYmc/ResuMesh) project.

## Installation

### From local source (development / monorepo)

```bash
pip install -e /path/to/resumesh-scrapers
```

### From the ResuMesh backend

```bash
cd backend
pip install -e ../../../resumesh-scrapers   # adjust relative path as needed
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
        pat="ghp_...",          # optional
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

## Backend Integration (ResuMesh)

### 1. Install the package

```bash
cd backend
pip install -e /path/to/resumesh-scrapers
```

### 2. Update imports in your backend

```python
# Before (tightly coupled)
from app.services.scrapers.base import IScraperService
from app.services.scrapers.exceptions import ScraperError
from app.services.scrapers.github_scraper import GitHubScraperService

# After (decoupled)
from resumesh_scrapers import GitHubScraperService, IScraperService
from resumesh_scrapers.exceptions import ScraperError
```

### 3. Map scraped data to your DB schemas

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

## License

AGPL-3.0 — see [LICENSE](LICENSE) for details.
