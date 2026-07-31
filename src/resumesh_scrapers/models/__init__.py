from resumesh_scrapers.models.behance import BehanceProjectModel
from resumesh_scrapers.models.devto import DevToArticleModel
from resumesh_scrapers.models.github import (
    GitHubCommitModel,
    GitHubLicense,
    GitHubOwner,
    GitHubRepositoryModel,
    GitHubUserModel,
)
from resumesh_scrapers.models.medium import MediumEntryModel
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
from resumesh_scrapers.models.substack import SubstackEntryModel
from resumesh_scrapers.models.youtube import YouTubeVideoModel

__all__ = [
    "DevToArticleModel",
    "MediumEntryModel",
    "SubstackEntryModel",
    "BehanceProjectModel",
    "GitHubLicense",
    "GitHubOwner",
    "GitHubRepositoryModel",
    "GitHubCommitModel",
    "GitHubUserModel",
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
    "YouTubeVideoModel",
]

