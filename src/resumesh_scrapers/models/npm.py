from typing import Any

from pydantic import BaseModel, Field


class NpmDownloads(BaseModel):
    monthly: int = 0
    weekly: int = 0


class NpmUser(BaseModel):
    username: str | None = None
    email: str | None = None


class NpmLinks(BaseModel):
    npm: str | None = None
    homepage: str | None = None
    repository: str | None = None
    bugs: str | None = None


class NpmPackage(BaseModel):
    name: str
    version: str
    description: str | None = None
    keywords: list[str] | None = None
    sanitized_name: str | None = None
    publisher: NpmUser | None = None
    maintainers: list[NpmUser] = Field(default_factory=list)
    license: str | None = None
    date: str | None = None
    links: NpmLinks | None = None


class NpmScoreDetail(BaseModel):
    popularity: float = 0.0
    quality: float = 0.0
    maintenance: float = 0.0


class NpmScore(BaseModel):
    final: float = 0.0
    detail: NpmScoreDetail | None = None


class NpmFlags(BaseModel):
    insecure: int | None = None
    unstable: bool | None = None
    deprecated: str | bool | None = None


class NpmSearchObject(BaseModel):
    package: NpmPackage
    downloads: NpmDownloads | None = None
    dependents: int = 0
    updated: str | None = None
    searchScore: float = Field(default=0.0, alias="searchScore")
    score: NpmScore | None = None
    flags: NpmFlags | dict[str, Any] | None = None


class NpmSearchResultModel(BaseModel):
    objects: list[NpmSearchObject] = Field(default_factory=list)
    total: int = 0
    time: str | None = None
