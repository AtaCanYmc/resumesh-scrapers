"""
ResuMesh Scrapers - Unified Provider Architecture Demo
======================================================
Demonstrates collecting, normalizing, and synchronizing developer profile
data across multiple platforms using unified domain models.
"""

import asyncio
from resumesh_scrapers import (
    DevToProvider,
    GitHubProvider,
    MediumProvider,
    ProviderRegistry,
    registry,
)


async def main():
    print("=== ResuMesh Scrapers: Provider Architecture Demo ===")

    # 1. Using Provider Registry
    available = registry.list_providers()
    print(f"Discovered Providers ({len(available)}): {', '.join(available)}")

    # 2. Fetch GitHub Profile & Projects
    github: GitHubProvider = registry.get_provider("github")
    profile = await github.get_profile("octocat")
    if profile:
        print(f"\n[GitHub Profile] {profile.name} (@{profile.username})")
        print(f"Bio: {profile.bio}")
        print(f"Website: {profile.website}")

    projects = await github.get_projects("octocat")
    print(f"Fetched {len(projects)} normalized projects from GitHub:")
    for proj in projects[:3]:
        print(f"  - {proj.name} ({proj.stars} ★ | {proj.language}): {proj.url}")

    # 3. Fetch Dev.to Articles
    devto: DevToProvider = registry.get_provider("devto")
    articles = await devto.get_articles("atacanymc")
    print(f"\n[Dev.to] Fetched {len(articles)} normalized articles:")
    for art in articles[:3]:
        print(f"  - {art.title} ({art.reading_time_minutes} min read) -> {art.url}")

    # 4. Fetch Medium Articles
    medium: MediumProvider = registry.get_provider("medium")
    medium_articles = await medium.get_articles("atacanymc")
    print(f"\n[Medium] Fetched {len(medium_articles)} normalized articles:")
    for art in medium_articles[:3]:
        print(f"  - {art.title} -> {art.url}")


if __name__ == "__main__":
    asyncio.run(main())
