"""Domain-specific exceptions for websum."""

from __future__ import annotations


class WebsumError(Exception):
    """Base exception for all websum errors."""


class BackendNotAvailableError(WebsumError):
    """Raised when a requested LLM backend's optional dependency is missing."""


class InvalidURLError(WebsumError):
    """Raised when a URL is malformed or does not match the expected format."""


class DocumentLoadError(WebsumError):
    """Raised when a document cannot be loaded from its source."""


class TranscriptUnavailableError(DocumentLoadError):
    """Raised when a YouTube transcript cannot be retrieved."""
