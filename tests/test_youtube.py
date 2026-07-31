import pytest
from unittest.mock import MagicMock, patch
from resumesh_scrapers.models import YouTubeVideoModel
from resumesh_scrapers.platforms import YouTubeScraperService
from resumesh_scrapers.exceptions import YouTubeScraperError

MOCK_INFO = {
    "id": "dQw4w9WgXcQ",
    "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up",
    "description": "Official Music Video",
    "duration": 213,
    "view_count": 1500000000,
    "like_count": 17000000,
    "comment_count": 2000000,
    "channel": "Rick Astley",
    "channel_id": "UCuAXFkgHJw83yv6f0e0hGWw",
    "uploader": "Rick Astley",
    "upload_date": "20091025",
    "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
    "categories": ["Music"],
    "tags": ["rick astley", "never gonna give you up"],
}


@pytest.mark.asyncio
async def test_youtube_scraper_fetch_video_success():
    scraper = YouTubeScraperService()
    
    with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = MOCK_INFO
        mock_ydl_cls.return_value.__enter__.return_value = mock_ydl
        
        result = await scraper.fetch_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        assert isinstance(result, YouTubeVideoModel)
        assert result.id == "dQw4w9WgXcQ"
        assert result.title == "Rick Astley - Never Gonna Give You Up"
        assert result.view_count == 1500000000
        assert result.channel == "Rick Astley"


@pytest.mark.asyncio
async def test_youtube_scraper_fetch_data_interface():
    scraper = YouTubeScraperService()
    
    with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = MOCK_INFO
        mock_ydl_cls.return_value.__enter__.return_value = mock_ydl
        
        results = await scraper.fetch_data("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        assert len(results) == 1
        assert results[0].id == "dQw4w9WgXcQ"


@pytest.mark.asyncio
async def test_youtube_scraper_error_handling():
    scraper = YouTubeScraperService()
    
    with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
        mock_ydl = MagicMock()
        mock_ydl.extract_info.side_effect = Exception("Video unavailable")
        mock_ydl_cls.return_value.__enter__.return_value = mock_ydl
        
        with pytest.raises(YouTubeScraperError):
            await scraper.fetch_video("https://www.youtube.com/watch?v=invalid_id")
