"""
Unit tests for Provider implementations using mock HTTP responses.
"""

import pytest
import respx
from httpx import Response
from resumesh_scrapers.providers import DevToProvider, GitHubProvider, MediumProvider


@pytest.mark.asyncio
@respx.mock
async def test_github_provider_get_profile():
    respx.get("https://api.github.com/users/octocat").mock(
        return_value=Response(
            200,
            json={
                "login": "octocat",
                "name": "The Octocat",
                "bio": "GitHub mascot",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "blog": "https://github.blog",
            },
        )
    )

    provider = GitHubProvider()
    profile = await provider.get_profile("octocat")

    assert profile is not None
    assert profile.platform == "github"
    assert profile.username == "octocat"
    assert profile.name == "The Octocat"
    assert profile.website == "https://github.blog"


@pytest.mark.asyncio
@respx.mock
async def test_github_provider_get_projects():
    respx.get("https://api.github.com/users/octocat/repos?per_page=100&sort=updated").mock(
        return_value=Response(
            200,
            json=[
                {
                    "name": "Hello-World",
                    "full_name": "octocat/Hello-World",
                    "description": "My first repo",
                    "html_url": "https://github.com/octocat/Hello-World",
                    "stargazers_count": 100,
                    "forks_count": 20,
                    "language": "Python",
                    "topics": ["octocat"],
                    "fork": False,
                }
            ],
        )
    )

    provider = GitHubProvider()
    projects = await provider.get_projects("octocat")

    assert len(projects) == 1
    assert projects[0].platform == "github"
    assert projects[0].name == "Hello-World"
    assert projects[0].stars == 100
    assert projects[0].language == "Python"


@pytest.mark.asyncio
@respx.mock
async def test_devto_provider_get_articles():
    respx.get("https://dev.to/api/articles?username=atacanymc&per_page=1000").mock(
        return_value=Response(
            200,
            json=[
                {
                    "title": "Clean Architecture in Python",
                    "url": "https://dev.to/atacanymc/clean-architecture",
                    "description": "A guide on architecture",
                    "published_at": "2024-01-01T12:00:00Z",
                    "tag_list": ["python", "architecture"],
                    "reading_time_minutes": 7,
                    "user": {"username": "atacanymc", "name": "Ata Can"},
                }
            ],
        )
    )

    provider = DevToProvider()
    articles = await provider.get_articles("atacanymc")

    assert len(articles) == 1
    assert articles[0].platform == "devto"
    assert articles[0].title == "Clean Architecture in Python"
    assert articles[0].reading_time_minutes == 7
    assert "python" in articles[0].tags


@pytest.mark.asyncio
@respx.mock
async def test_medium_provider_get_articles():
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Stories by @atacanymc on Medium</title>
            <link>https://medium.com/@atacanymc</link>
            <item>
                <title>Designing Pluggable Libraries</title>
                <link>https://medium.com/@atacanymc/designing-pluggable-libraries-12345?source=rss</link>
                <description><![CDATA[<p>Summary of post</p>]]></description>
                <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
            </item>
        </channel>
    </rss>
    """
    respx.get("https://medium.com/feed/@atacanymc").mock(
        return_value=Response(200, text=sample_xml)
    )

    provider = MediumProvider()
    articles = await provider.get_articles("atacanymc")

    assert len(articles) == 1
    assert articles[0].platform == "medium"
    assert articles[0].title == "Designing Pluggable Libraries"
    assert articles[0].url == "https://medium.com/@atacanymc/designing-pluggable-libraries-12345"
