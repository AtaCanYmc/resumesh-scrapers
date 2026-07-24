from typing import Any, List, Optional
from pydantic import BaseModel, Field


class LinkModel(BaseModel):
    rel: Optional[str] = None
    type: Optional[str] = None
    href: Optional[str] = None


class TagModel(BaseModel):
    term: Optional[str] = None
    scheme: Optional[str] = None
    label: Optional[str] = None


class AuthorDetailModel(BaseModel):
    name: Optional[str] = None


class ContentModel(BaseModel):
    type: Optional[str] = None
    language: Optional[str] = None
    base: Optional[str] = None
    value: Optional[str] = None


class TitleDetailModel(BaseModel):
    type: Optional[str] = None
    language: Optional[str] = None
    base: Optional[str] = None
    value: Optional[str] = None


class MediumEntryModel(BaseModel):
    title: str
    title_detail: Optional[TitleDetailModel] = None
    links: List[LinkModel] = Field(default_factory=list)
    link: Optional[str] = None
    id: Optional[str] = None
    guidislink: Optional[bool] = False
    tags: List[TagModel] = Field(default_factory=list)
    authors: List[AuthorDetailModel] = Field(default_factory=list)
    author: Optional[str] = None
    author_detail: Optional[AuthorDetailModel] = None
    published: Optional[str] = None
    published_parsed: Optional[Any] = None
    updated: Optional[str] = None
    updated_parsed: Optional[Any] = None
    content: List[ContentModel] = Field(default_factory=list)
    summary: Optional[str] = None
