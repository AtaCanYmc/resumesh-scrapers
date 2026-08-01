from typing import Any, Optional, Union

from pydantic import BaseModel, Field


class NpmDownloads(BaseModel):
    monthly: int = 0
    weekly: int = 0


class NpmUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class NpmLinks(BaseModel):
    npm: Optional[str] = None
    homepage: Optional[str] = None
    repository: Optional[str] = None
    bugs: Optional[str] = None


class NpmPackage(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    keywords: Optional[list[str]] = None
    sanitized_name: Optional[str] = None
    publisher: Optional[NpmUser] = None
    maintainers: list[NpmUser] = Field(default_factory=list)
    license: Optional[str] = None
    date: Optional[str] = None
    links: Optional[NpmLinks] = None


class NpmScoreDetail(BaseModel):
    popularity: float = 0.0
    quality: float = 0.0
    maintenance: float = 0.0


class NpmScore(BaseModel):
    final: float = 0.0
    detail: Optional[NpmScoreDetail] = None


class NpmFlags(BaseModel):
    insecure: Optional[int] = None
    unstable: Optional[bool] = None
    deprecated: Optional[Union[str, bool]] = None


class NpmSearchObject(BaseModel):
    package: NpmPackage
    downloads: Optional[NpmDownloads] = None
    dependents: int = 0
    updated: Optional[str] = None
    searchScore: float = Field(default=0.0, alias="searchScore")
    score: Optional[NpmScore] = None
    flags: Optional[Union[NpmFlags, dict[str, Any]]] = None


class NpmSearchResultModel(BaseModel):
    objects: list[NpmSearchObject] = Field(default_factory=list)
    total: int = 0
    time: Optional[str] = None
