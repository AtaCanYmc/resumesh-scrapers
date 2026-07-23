"""
Scraper-specific exception hierarchy.

Usage:
    from resumesh_scrapers.exceptions import GitHubScraperError

    raise GitHubScraperError("API rate limit exceeded", status_code=403)
"""


class ScraperError(Exception):
    """Base exception for all scraper services."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        if self.status_code:
            return f"[HTTP {self.status_code}] {self.message}"
        return self.message


class GitHubScraperError(ScraperError):
    """Raised when the GitHub API returns an error or unexpected response."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class MediumScraperError(ScraperError):
    """Raised when the Medium RSS feed cannot be fetched or parsed."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class DevToScraperError(ScraperError):
    """Raised when the Dev.to API returns an error or unexpected response."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class NetworkError(ScraperError):
    """Raised during network connectivity issues, timeouts, or HTTP connection errors."""

    def __init__(self, message: str = "An error occurred during the network connection."):
        super().__init__(message)
        self.message = message
        self.status_code = 500


class RateLimitError(ScraperError):
    """Raised when hitting a rate limit imposed by the target platform."""

    def __init__(self, message: str = "Platform rate limit has been exceeded."):
        super().__init__(message)
        self.message = message
        self.status_code = 503


class ParsingError(ScraperError):
    """Raised when the structure breaks during HTML parsing or data configuration processes."""

    def __init__(self, message: str = "An error occurred while processing or parsing data."):
        super().__init__(message)
        self.message = message
        self.status_code = 500
