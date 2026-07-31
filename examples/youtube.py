import asyncio
import logging

from resumesh_scrapers.exceptions import YouTubeScraperError
from resumesh_scrapers.platforms.youtube import YouTubeScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    # Example YouTube Video URL
    video_url = "https://www.youtube.com/watch?v=NQBR6YZ-G9c"
    try:
        logger.info(f"Fetching YouTube video data for URL: {video_url}")
        youtube_scraper = YouTubeScraper()

        # Fetch video metadata
        video_data = await youtube_scraper.fetch_video(video_url)

        logger.info("Successfully fetched YouTube video metadata:")
        logger.info(f"- Title: {video_data.title}")
        logger.info(f"- Channel: {video_data.channel} ({video_data.channel_url})")
        logger.info(f"- Views: {video_data.view_count:,}" if video_data.view_count else "- Views: N/A")
        logger.info(f"- Likes: {video_data.like_count:,}" if video_data.like_count else "- Likes: N/A")
        logger.info(f"- Duration: {video_data.duration} seconds" if video_data.duration else "- Duration: N/A")
        logger.info(f"- Thumbnail: {video_data.thumbnail}")
        logger.info(f"- Tags: {', '.join(video_data.tags[:5])}" if video_data.tags else "- Tags: None")

    except YouTubeScraperError as e:
        logger.error(f"YouTube scraper error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
