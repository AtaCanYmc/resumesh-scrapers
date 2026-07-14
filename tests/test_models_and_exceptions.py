"""Tests for Pydantic models and exception hierarchy."""

import pytest

from resumesh_scrapers.exceptions import (
    DevToScraperError,
    GitHubScraperError,
    MediumScraperError,
    ScraperError,
)
from resumesh_scrapers.models import ArticlePlatform, ScrapedArticle, ScrapedProject


# ── Models ──────────────────────────────────────────────────────────────────


class TestScrapedProject:
    def test_minimal(self):
        project = ScrapedProject(title="my-repo")
        assert project.title == "my-repo"
        assert project.stars == 0
        assert project.languages == []
        assert project.tags == []
        assert project.description is None
        assert project.github_url is None

    def test_full(self):
        project = ScrapedProject(
            title="ResuMesh",
            description="Portfolio manager",
            github_url="https://github.com/AtaCanYmc/ResuMesh",
            stars=42,
            watchers=10,
            forks=5,
            languages=["Python", "TypeScript"],
            tags=["portfolio", "cv"],
            raw_github_data={"id": 123},
            created_at="2024-01-01T00:00:00Z",
        )
        assert project.stars == 42
        assert project.languages == ["Python", "TypeScript"]
        assert str(project.github_url) == "https://github.com/AtaCanYmc/ResuMesh"

    def test_model_dump_roundtrip(self):
        project = ScrapedProject(
            title="test",
            github_url="https://github.com/test/test",
            stars=1,
        )
        data = project.model_dump()
        assert data["title"] == "test"
        assert data["stars"] == 1
        reconstructed = ScrapedProject(**data)
        assert reconstructed.title == project.title


class TestScrapedArticle:
    def test_minimal(self):
        article = ScrapedArticle(
            title="My Article",
            url="https://dev.to/user/my-article",
            platform=ArticlePlatform.DEV_TO,
        )
        assert article.title == "My Article"
        assert article.platform == ArticlePlatform.DEV_TO
        assert article.reading_time_minutes == 0

    def test_medium_article(self):
        article = ScrapedArticle(
            title="Medium Post",
            url="https://medium.com/@user/my-post-abc123",
            platform=ArticlePlatform.MEDIUM,
            summary="A great post",
            reading_time_minutes=5,
            published_at="2024-06-15T12:00:00Z",
            raw_platform_data={"tags": ["python", "ai"]},
        )
        assert article.platform == ArticlePlatform.MEDIUM
        assert article.reading_time_minutes == 5
        assert article.raw_platform_data["tags"] == ["python", "ai"]


class TestArticlePlatform:
    def test_values(self):
        assert ArticlePlatform.MEDIUM == "MEDIUM"
        assert ArticlePlatform.DEV_TO == "DEV_TO"

    def test_is_str_enum(self):
        assert isinstance(ArticlePlatform.MEDIUM, str)


# ── Exceptions ──────────────────────────────────────────────────────────────


class TestExceptions:
    def test_scraper_error_message_only(self):
        err = ScraperError("something failed")
        assert str(err) == "something failed"
        assert err.status_code is None
        assert err.message == "something failed"

    def test_scraper_error_with_status_code(self):
        err = ScraperError("rate limited", status_code=429)
        assert str(err) == "[HTTP 429] rate limited"
        assert err.status_code == 429

    def test_github_error_is_scraper_error(self):
        err = GitHubScraperError("not found", status_code=404)
        assert isinstance(err, ScraperError)
        assert err.status_code == 404

    def test_medium_error_is_scraper_error(self):
        err = MediumScraperError("feed error")
        assert isinstance(err, ScraperError)

    def test_devto_error_is_scraper_error(self):
        err = DevToScraperError("api error", status_code=500)
        assert isinstance(err, ScraperError)

    def test_catch_all_with_base_class(self):
        """All platform errors should be catchable via ScraperError."""
        errors = [
            GitHubScraperError("gh"),
            MediumScraperError("med"),
            DevToScraperError("dev"),
        ]
        for err in errors:
            with pytest.raises(ScraperError):
                raise err
