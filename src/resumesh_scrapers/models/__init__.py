from resumesh_scrapers.models.behance import BehanceProjectModel
from resumesh_scrapers.models.devto import DevToArticleModel
from resumesh_scrapers.models.github import (
    GitHubLicense,
    GitHubOwner,
    GitHubRepositoryModel,
)
from resumesh_scrapers.models.medium import MediumEntryModel
from resumesh_scrapers.models.substack import SubstackEntryModel
from resumesh_scrapers.models.npm import (
    NpmDownloads,
    NpmFlags,
    NpmLinks,
    NpmPackage,
    NpmScore,
    NpmScoreDetail,
    NpmSearchObject,
    NpmSearchResultModel,
    NpmUser,
)
from resumesh_scrapers.models.pypi import (
    Digests,
    Info,
    InfoDownloads,
    Ownership,
    PyPiPackageModel,
    ReleaseFile,
    Role,
)

__all__ = [
    "DevToArticleModel",
    "MediumEntryModel",
    "SubstackEntryModel",
    "BehanceProjectModel",
    "GitHubLicense",
    "GitHubOwner",
    "GitHubRepositoryModel",
    "NpmDownloads",
    "NpmFlags",
    "NpmLinks",
    "NpmPackage",
    "NpmScore",
    "NpmScoreDetail",
    "NpmSearchObject",
    "NpmSearchResultModel",
    "NpmUser",
    "Digests",
    "Info",
    "InfoDownloads",
    "Ownership",
    "PyPiPackageModel",
    "ReleaseFile",
    "Role",
]
