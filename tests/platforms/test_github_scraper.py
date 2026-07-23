"""Tests for GitHubScraperService."""

import httpx
import pytest
import respx
from httpx import Response
from resumesh_scrapers.exceptions import GitHubScraperError
from resumesh_scrapers.models import GitHubRepositoryModel
from resumesh_scrapers.platforms import GitHubScraperService

# ── Fixtures ────────────────────────────────────────────────────────────────

SAMPLE_REPOS = [
    {
        "name": "ResuMesh",
        "html_url": "https://github.com/octocat/ResuMesh",
        "description": "Portfolio manager",
        "language": "Python",
        "stargazers_count": 42,
        "watchers_count": 10,
        "forks_count": 5,
        "fork": False,
        "created_at": "2024-01-15T10:00:00Z",
    },
    {
        "name": "forked-repo",
        "html_url": "https://github.com/octocat/forked-repo",
        "description": "A fork",
        "language": "JavaScript",
        "stargazers_count": 0,
        "watchers_count": 0,
        "forks_count": 0,
        "fork": True,
        "created_at": "2024-02-01T00:00:00Z",
    },
    {
        "name": "no-lang-repo",
        "html_url": "https://github.com/octocat/no-lang-repo",
        "description": None,
        "language": None,
        "stargazers_count": 1,
        "watchers_count": 1,
        "forks_count": 0,
        "fork": False,
        "created_at": "2024-03-01T00:00:00Z",
    },
]


@pytest.fixture
def scraper():
    return GitHubScraperService()


# ── Tests ───────────────────────────────────────────────────────────────────


class TestGitHubScraperFetchData:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_repos_success(self, scraper):
        respx.get("https://api.github.com/users/octocat/repos").mock(return_value=Response(200, json=SAMPLE_REPOS))

        projects = await scraper.fetch_data("octocat")

        assert len(projects) == 2  # fork excluded
        assert all(isinstance(p, GitHubRepositoryModel) for p in projects)
        assert projects[0].name == "ResuMesh"
        assert projects[0].stargazers_count == 42
        assert projects[0].language == "Python"

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_repos_include_forks(self, scraper):
        respx.get("https://api.github.com/users/octocat/repos").mock(return_value=Response(200, json=SAMPLE_REPOS))

        projects = await scraper.fetch_data("octocat", include_forks=True)

        assert len(projects) == 3  # fork included

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_repos_empty(self, scraper):
        respx.get("https://api.github.com/users/octocat/repos").mock(return_value=Response(200, json=[]))

        projects = await scraper.fetch_data("octocat")
        assert projects == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_repos_http_error(self, scraper):
        respx.get("https://api.github.com/users/octocat/repos").mock(return_value=Response(404, text="Not Found"))

        with pytest.raises(GitHubScraperError) as exc_info:
            await scraper.fetch_data("octocat")

        assert exc_info.value.status_code == 404

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_repos_network_error(self, scraper):
        respx.get("https://api.github.com/users/octocat/repos").mock(
            side_effect=httpx.ConnectError("connection refused")
        )

        with pytest.raises(GitHubScraperError, match="Network error"):
            await scraper.fetch_data("octocat")

    @pytest.mark.asyncio
    async def test_invalid_username(self, scraper):
        with pytest.raises(GitHubScraperError, match="Invalid GitHub username"):
            await scraper.fetch_data("invalid user!")

    @respx.mock
    @pytest.mark.asyncio
    async def test_repo_without_language(self, scraper):
        respx.get("https://api.github.com/users/octocat/repos").mock(return_value=Response(200, json=[SAMPLE_REPOS[2]]))

        projects = await scraper.fetch_data("octocat")
        assert projects[0].languages == []
        assert "no-lang-repo" in projects[0].tags


class TestGitHubScraperParseRepo:
    def test_parse_repo_fields(self):
        project = GitHubScraperService._parse_repo(SAMPLE_REPOS[0])

        assert project.name == "ResuMesh"
        assert project.description == "Portfolio manager"
        assert str(project.html_url) == "https://github.com/octocat/ResuMesh"
        assert project.stargazers_count == 42
        assert project.watchers_count == 10
        assert project.forks_count == 5
        assert "Python" in project.languages
        assert "resumesh" in project.tags

    def test_parse_repo_no_language(self):
        project = GitHubScraperService._parse_repo(SAMPLE_REPOS[2])
        assert project.languages == []


class TestGitHubScraperHeaders:
    def test_headers_without_pat(self):
        headers = GitHubScraperService._build_headers()
        assert "User-Agent" in headers
        assert "Authorization" not in headers

    def test_headers_with_pat(self):
        headers = GitHubScraperService._build_headers(pat="ghp_test123")
        assert headers["Authorization"] == "Bearer ghp_test123"
