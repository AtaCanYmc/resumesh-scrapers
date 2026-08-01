"""
Unit tests for normalized domain models.
"""

from datetime import datetime

from resumesh_scrapers.domain import Article, Experience, Profile, Project, Skill, Video


def test_profile_domain_model():
    profile = Profile(
        platform="github",
        username="octocat",
        name="The Octocat",
        bio="GitHub mascot",
        avatar_url="https://github.com/images/error/octocat_happy.gif",
        location="San Francisco",
        company="GitHub",
        website="https://github.blog",
        social_links={"github": "https://github.com/octocat"},
    )
    assert profile.platform == "github"
    assert profile.username == "octocat"
    assert profile.name == "The Octocat"
    assert profile.social_links["github"] == "https://github.com/octocat"


def test_project_domain_model():
    project = Project(
        platform="github",
        name="Hello-World",
        description="My first repository",
        url="https://github.com/octocat/Hello-World",
        stars=42,
        forks=10,
        language="Python",
        topics=["octocat", "sample"],
    )
    assert project.name == "Hello-World"
    assert project.stars == 42
    assert project.language == "Python"
    assert "octocat" in project.topics


def test_article_domain_model():
    now = datetime.now()
    article = Article(
        platform="devto",
        title="Python 3.12 Tips",
        url="https://dev.to/octocat/python-tips",
        summary="A short summary",
        published_at=now,
        tags=["python", "dev"],
        reading_time_minutes=5,
    )
    assert article.title == "Python 3.12 Tips"
    assert article.reading_time_minutes == 5
    assert article.tags == ["python", "dev"]


def test_video_domain_model():
    video = Video(
        platform="youtube",
        title="Python Clean Architecture Tutorial",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        duration_seconds=600,
        view_count=1000,
        like_count=150,
        tags=["python", "tutorial"],
    )
    assert video.platform == "youtube"
    assert video.title == "Python Clean Architecture Tutorial"
    assert video.duration_seconds == 600
    assert video.view_count == 1000


def test_experience_domain_model():
    exp = Experience(
        platform="github",
        role="Maintainer",
        organization="ResuMesh",
        skills=["Python", "FastAPI"],
    )
    assert exp.role == "Maintainer"
    assert exp.organization == "ResuMesh"
    assert "Python" in exp.skills


def test_skill_domain_model():
    skill = Skill(platform="github", name="Python", category="Language")
    assert skill.name == "Python"
    assert skill.category == "Language"
