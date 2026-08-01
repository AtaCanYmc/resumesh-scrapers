from typing import Any, Optional, Union

from pydantic import BaseModel, Field


class InfoDownloads(BaseModel):
    last_day: int
    last_month: int
    last_week: int


class Info(BaseModel):
    author: Optional[str] = None
    author_email: Optional[str] = None
    bugtrack_url: Optional[str] = None
    classifiers: Optional[list[str]] = None
    description: Optional[str] = None
    description_content_type: Optional[str] = None
    docs_url: Optional[str] = None
    download_url: Optional[str] = None
    downloads: InfoDownloads
    dynamic: Optional[Any] = None
    home_page: Optional[str] = None
    keywords: Optional[str] = None
    license: Optional[str] = None
    license_expression: Optional[str] = None
    license_files: Optional[list[str]] = None
    maintainer: Optional[str] = None
    maintainer_email: Optional[str] = None
    name: str
    package_url: Optional[str] = None
    platform: Optional[str] = None
    project_url: Optional[str] = None
    project_urls: Optional[dict[str, str]] = None
    provides_extra: Optional[list[str]] = None
    release_url: Optional[str] = None
    requires_dist: Optional[list[str]] = None
    requires_python: Optional[str] = None
    summary: Optional[str] = None
    version: str
    yanked: bool = False
    yanked_reason: Optional[str] = None


class Digests(BaseModel):
    blake2b_256: str
    md5: str
    sha256: str


class ReleaseFile(BaseModel):
    comment_text: Optional[str] = None
    core_metadata: Optional[Union[dict, bool]] = Field(default=None, alias="core-metadata")
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: Optional[str] = None
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    yanked: bool
    yanked_reason: Optional[str] = None


class Role(BaseModel):
    role: str
    user: str


class Ownership(BaseModel):
    organization: Optional[str] = None
    roles: list[Role]


class PyPiPackageModel(BaseModel):
    info: Info
    last_serial: int
    ownership: Ownership
    releases: dict[str, list[ReleaseFile]]
    urls: list[ReleaseFile]
    vulnerabilities: Optional[list[Any]] = None
