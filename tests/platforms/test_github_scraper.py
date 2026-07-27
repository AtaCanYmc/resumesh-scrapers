"""Tests for GitHubScraperService."""

import httpx
import pytest
import respx
from httpx import Response
from resumesh_scrapers.exceptions import GitHubScraperError
from resumesh_scrapers.models import GitHubCommitModel, GitHubRepositoryModel
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

SAMPLE_COMMITS = {
    "total_count": 2,
    "incomplete_results": False,
    "items": [
        {
            "sha": "abcdef1234567890",
            "commit": {
                "author": {
                    "name": "Octocat",
                    "email": "octocat@github.com",
                    "date": "2026-07-27T12:00:00Z"
                },
                "message": "feat: add super cool feature",
                "url": "https://api.github.com/repos/octocat/ResuMesh/git/commits/abcdef1234567890"
            },
            "html_url": "https://github.com/octocat/ResuMesh/commit/abcdef1234567890",
            "repository": {
                "name": "ResuMesh",
                "full_name": "octocat/ResuMesh"
            }
        },
        {
            "sha": "1234567890abcdef",
            "commit": {
                "author": {
                    "name": "Octocat",
                    "email": "octocat@github.com",
                    "date": "2026-07-26T15:30:00Z"
                },
                "message": "fix: resolve bug",
                "url": "https://api.github.com/repos/octocat/ResuMesh/git/commits/1234567890abcdef"
            },
            "html_url": "https://github.com/octocat/ResuMesh/commit/1234567890abcdef",
            "repository": {
                "name": "ResuMesh",
                "full_name": "octocat/ResuMesh"
            }
        }
    ]
}



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


class TestGitHubScraperFetchReadmeRepo:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_readme_repo_success(self, scraper):
        respx.get("https://api.github.com/repos/octocat/octocat").mock(
            return_value=Response(200, json=SAMPLE_REPOS[0])
        )

        repo = await scraper.fetch_readme_repo("octocat")
        assert repo is not None
        assert repo.name == "ResuMesh"

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_readme_repo_not_found(self, scraper):
        respx.get("https://api.github.com/repos/octocat/octocat").mock(
            return_value=Response(404, text="Not Found")
        )

        repo = await scraper.fetch_readme_repo("octocat")
        assert repo is None

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_readme_repo_http_error(self, scraper):
        respx.get("https://api.github.com/repos/octocat/octocat").mock(
            return_value=Response(500, text="Internal Server Error")
        )

        with pytest.raises(GitHubScraperError) as exc_info:
            await scraper.fetch_readme_repo("octocat")
        assert exc_info.value.status_code == 500


class TestGitHubScraperFetchCommits:
    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_commits_success(self, scraper):
        respx.get("https://api.github.com/search/commits").mock(
            return_value=Response(200, json=SAMPLE_COMMITS)
        )

        commits = await scraper.fetch_data("octocat")  # Wait, wait! The method name is fetch_commits!
        # Let's verify: we want to call fetch_commits!
        commits = await scraper.fetch_commits("octocat")

        assert len(commits) == 2
        assert all(isinstance(c, GitHubCommitModel) for c in commits)
        assert commits[0].sha == "abcdef1234567890"
        assert commits[0].message == "feat: add super cool feature"
        assert commits[0].author_name == "Octocat"
        assert commits[0].repo_name == "ResuMesh"
        assert commits[0].repo_full_name == "octocat/ResuMesh"
        assert commits[0].html_url == "https://github.com/octocat/ResuMesh/commit/abcdef1234567890"

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_commits_empty(self, scraper):
        respx.get("https://api.github.com/search/commits").mock(
            return_value=Response(200, json={"total_count": 0, "items": []})
        )

        commits = await scraper.fetch_commits("octocat")
        assert commits == []

    @respx.mock
    @pytest.mark.asyncio
    async def test_fetch_commits_http_error(self, scraper):
        respx.get("https://api.github.com/search/commits").mock(
            return_value=Response(404, text="Not Found")
        )

        with pytest.raises(GitHubScraperError) as exc_info:
            await scraper.fetch_commits("octocat")

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_username_commits(self, scraper):
        with pytest.raises(GitHubScraperError, match="Invalid GitHub username"):
            await scraper.fetch_commits("invalid user!")


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
