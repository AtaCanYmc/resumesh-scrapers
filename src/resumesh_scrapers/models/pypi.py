from typing import Any

from pydantic import BaseModel, Field


class InfoDownloads(BaseModel):
    last_day: int
    last_month: int
    last_week: int


class Info(BaseModel):
    author: str | None = None
    author_email: str | None = None
    bugtrack_url: str | None = None
    classifiers: list[str] | None = None
    description: str | None = None
    description_content_type: str | None = None
    docs_url: str | None = None
    download_url: str | None = None
    downloads: InfoDownloads
    dynamic: Any | None = None
    home_page: str | None = None
    keywords: str | None = None
    license: str | None = None
    license_expression: str | None = None
    license_files: list[str] | None = None
    maintainer: str | None = None
    maintainer_email: str | None = None
    name: str
    package_url: str | None = None
    platform: str | None = None
    project_url: str | None = None
    project_urls: dict[str, str] | None = None
    provides_extra: list[str] | None = None
    release_url: str | None = None
    requires_dist: list[str] | None = None
    requires_python: str | None = None
    summary: str | None = None
    version: str
    yanked: bool = False
    yanked_reason: str | None = None


class Digests(BaseModel):
    blake2b_256: str
    md5: str
    sha256: str


class ReleaseFile(BaseModel):
    comment_text: str | None = None
    core_metadata: dict | bool | None = Field(default=None, alias="core-metadata")
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str | None = None
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    yanked: bool
    yanked_reason: str | None = None


class Role(BaseModel):
    role: str
    user: str


class Ownership(BaseModel):
    organization: str | None = None
    roles: list[Role]


class PyPiPackageModel(BaseModel):
    info: Info
    last_serial: int
    ownership: Ownership
    releases: dict[str, list[ReleaseFile]]
    urls: list[ReleaseFile]
    vulnerabilities: list[Any] | None = None
