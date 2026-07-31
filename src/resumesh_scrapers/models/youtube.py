from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class YouTubeVideoModel(BaseModel):
    """Pydantic data model for YouTube video metadata extracted via yt-dlp."""

    id: str = Field(description="YouTube Video ID")
    url: Optional[str] = Field(default=None, description="Direct or watch URL of the video")
    title: str = Field(description="Title of the video")
    description: Optional[str] = Field(default=None, description="Description text of the video")
    duration: Optional[int] = Field(default=None, description="Duration of the video in seconds")
    view_count: Optional[int] = Field(default=None, description="Total view count")
    like_count: Optional[int] = Field(default=None, description="Total like count")
    comment_count: Optional[int] = Field(default=None, description="Total comment count")
    channel: Optional[str] = Field(default=None, description="Name of the channel")
    channel_id: Optional[str] = Field(default=None, description="ID of the channel")
    channel_url: Optional[str] = Field(default=None, description="URL of the channel")
    uploader: Optional[str] = Field(default=None, description="Name of the uploader")
    upload_date: Optional[str] = Field(default=None, description="Upload date in YYYYMMDD format")
    thumbnail: Optional[str] = Field(default=None, description="Thumbnail image URL")
    categories: list[str] = Field(default_factory=list, description="Categories assigned to the video")
    tags: list[str] = Field(default_factory=list, description="Tags assigned to the video")

    model_config = ConfigDict(extra="ignore", populate_by_name=True)
