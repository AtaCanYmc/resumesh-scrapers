"""Tests for Pydantic models and exception hierarchy."""

import pytest
from resumesh_scrapers.exceptions import (
    DevToScraperError,
    GitHubScraperError,
    MediumScraperError,
    ScraperError,
)
from resumesh_scrapers.models import (
    GitHubRepositoryModel,
    MediumEntryModel
)


# ── Models ──────────────────────────────────────────────────────────────────


class TestScrapedProject:
    def test_minimal(self):
        project = GitHubRepositoryModel(name="my-repo")
        assert project.name == "my-repo"
        assert project.stargazers_count == 0
        assert project.languages == []
        assert project.tags == []
        assert project.description is None
        assert project.html_url is None

    def test_full(self):
        project = GitHubRepositoryModel(
            name="ResuMesh",
            url="https://github.com/ResuMesh/ResuMesh",
            description="ResuMesh",
            stargazers_count=42,
            language="Python",
        )
        assert project.stargazers_count == 42
        assert project.language == "Python"
        assert str(project.url) == "https://github.com/ResuMesh/ResuMesh"

    def test_model_dump_roundtrip(self):
        project = GitHubRepositoryModel(
            name="test",
            url="https://github.com/test/test",
            stargazers_count=1,
        )
        data = project.model_dump()
        assert data["name"] == "test"
        assert data["stargazers_count"] == 1
        reconstructed = GitHubRepositoryModel(**data)
        assert reconstructed.name == project.name
        assert reconstructed.stargazers_count == project.stargazers_count


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
