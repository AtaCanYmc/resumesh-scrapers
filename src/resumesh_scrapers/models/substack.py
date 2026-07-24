from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LinkModel(BaseModel):
    rel: Optional[str] = None
    type: Optional[str] = None
    href: Optional[str] = None


class TagModel(BaseModel):
    term: Optional[str] = None
    scheme: Optional[str] = None
    label: Optional[str] = None


class SubstackEntryModel(BaseModel):
    title: str
    link: Optional[str] = None
    links: List[LinkModel] = Field(default_factory=list)
    id: Optional[str] = None
    guidislink: Optional[bool] = False
    tags: List[TagModel] = Field(default_factory=list)
    published: Optional[str] = None
    published_parsed: Optional[Any] = None
    summary: Optional[str] = None

    model_config = ConfigDict(extra="ignore")
