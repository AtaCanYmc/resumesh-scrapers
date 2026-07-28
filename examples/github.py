import asyncio
import logging

from resumesh_scrapers.exceptions import ScraperError
from resumesh_scrapers.platforms.github import GitHubScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    username = "octocat"
    try:
        logger.info(f"Fetching GitHub data for: {username}")
        github_scraper = GitHubScraper()

        # 1. Fetch repositories
        github_data = await github_scraper.fetch_data(username)
        logger.info(f"GitHub success: {len(github_data)} repositories found.")
        for repo in github_data[:2]:
            logger.info(f"- Repo: {repo.name} (Stars: {repo.stargazers_count})")

        # 2. Fetch special Profile README Repo
        readme_repo = await github_scraper.fetch_readme_repo(username)
        if readme_repo:
            logger.info(f"Profile README Repository exists: {readme_repo.html_url}")
        else:
            logger.info("No Profile README Repository found.")

        # 3. Fetch recent commits (weekly default)
        commits = await github_scraper.fetch_commits(username)
        logger.info(f"Recent commits found: {len(commits)}")
        for commit in commits[:2]:
            logger.info(f"- Commit: [{commit.sha[:7]}] {commit.message} in {commit.repo_name}")

        # 4. Fetch followers and following
        followers = await github_scraper.fetch_followers(username, per_page=10)
        following = await github_scraper.fetch_following(username, per_page=10)
        logger.info(f"Followers: {len(followers)}, Following: {len(following)}")
        if followers:
            logger.info(f"- First follower: {followers[0].login}")
        if following:
            logger.info(f"- First following: {following[0].login}")

    except ScraperError as e:
        logger.error(f"GitHub scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

