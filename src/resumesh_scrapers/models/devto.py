from typing import List, Optional, Union
from pydantic import BaseModel, Field


class DevToUser(BaseModel):
    name: str
    username: str
    user_id: int
    twitter_username: Optional[str] = None
    github_username: Optional[str] = None
    website_url: Optional[str] = None
    profile_image: Optional[str] = None
    profile_image_90: Optional[str] = None


class DevToArticleModel(BaseModel):
    id: int
    title: str
    type_of: str = "article"
    description: Optional[str] = None
    readable_publish_date: Optional[str] = None
    slug: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    comments_count: int = 0
    public_reactions_count: int = 0
    positive_reactions_count: int = 0
    collection_id: Optional[Union[int, str]] = None
    published_timestamp: Optional[str] = None
    language: Optional[str] = None
    subforem_id: Optional[int] = None
    cover_image: Optional[str] = None
    social_image: Optional[str] = None
    canonical_url: Optional[str] = None
    created_at: Optional[str] = None
    edited_at: Optional[str] = None
    crossposted_at: Optional[str] = None
    published_at: Optional[str] = None
    last_comment_at: Optional[str] = None
    reading_time_minutes: int = 0
    tag_list: List[str] = Field(default_factory=list)
    tags: Optional[str] = None
    user: DevToUser
