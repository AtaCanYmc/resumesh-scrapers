from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class BehanceProjectModel(BaseModel):
    """Pydantic model for raw project data fetched or parsed from Behance."""

    id: Optional[str] = None
    name: str
    url: HttpUrl
    published_on: Optional[datetime] = None
    stats_appreciations: int = 0
    stats_views: int = 0
    covers_url: Optional[HttpUrl | str] = None
    tags: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")
