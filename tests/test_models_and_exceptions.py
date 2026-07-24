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
    MediumEntryModel,
    SubstackEntryModel
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


class TestMediumEntryModel:
    def test_minimal(self):
        entry = MediumEntryModel(title="My Article", link="https://medium.com/@user/my-article")
        assert entry.title == "My Article"
        assert entry.link == "https://medium.com/@user/my-article"
        assert entry.tags == []

    def test_full(self):
        entry = MediumEntryModel(
            title="Medium Post",
            link="https://medium.com/@user/my-post-abc123",
            summary="A great post",
            tags=[{"term": "python"}, {"term": "ai"}],
        )
        assert entry.summary == "A great post"
        assert [t.term for t in entry.tags] == ["python", "ai"]


class TestSubstackEntryModel:
    def test_minimal(self):
        entry = SubstackEntryModel(title="My Substack Post", link="https://atacan.substack.com/p/post")
        assert entry.title == "My Substack Post"
        assert entry.link == "https://atacan.substack.com/p/post"
        assert entry.tags == []


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
