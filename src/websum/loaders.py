"""Document loaders for web pages and YouTube videos."""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from .exceptions import DocumentLoadError, InvalidURLError, TranscriptUnavailableError

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger = logging.getLogger(__name__)

_YOUTUBE_REGEX = re.compile(
    r"^(?:https?://)?(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-]+)(?:\?.*)?$"
)


def is_youtube_url(url: str) -> bool:
    """Return True when `url` looks like a YouTube video URL."""
    return _YOUTUBE_REGEX.match(url) is not None


def load_web_document(url: str) -> list[Document]:
    """Load a web page as LangChain Documents.

    Raises:
        DocumentLoadError: if the page cannot be fetched or parsed.
    """
    from langchain_community.document_loaders import WebBaseLoader

    logger.debug("Loading web document: %s", url)
    try:
        loader = WebBaseLoader(url)
        return loader.load()
    except Exception as exc:
        raise DocumentLoadError(f"Failed to load web document at {url}: {exc}") from exc


def load_youtube_transcript(
    url: str,
    languages: tuple[str, ...] = ("en", "en-US"),
) -> list[Document]:
    """Load a YouTube transcript as LangChain Documents.

    Raises:
        InvalidURLError: if `url` is not a YouTube URL.
        TranscriptUnavailableError: if the transcript cannot be retrieved.
    """
    if not is_youtube_url(url):
        raise InvalidURLError(f"Not a valid YouTube URL: {url}")

    from langchain_community.document_loaders import YoutubeLoader

    logger.debug("Loading YouTube transcript: %s", url)
    try:
        loader = YoutubeLoader.from_youtube_url(url, language=list(languages))
        return loader.load()
    except Exception as exc:
        raise TranscriptUnavailableError(f"Failed to retrieve transcript for {url}: {exc}") from exc
