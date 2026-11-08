"""Document loaders for web pages and YouTube videos."""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING
from urllib.parse import parse_qs, urlsplit

from .exceptions import DocumentLoadError, InvalidURLError, TranscriptUnavailableError

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger = logging.getLogger(__name__)

_VIDEO_ID = re.compile(r"[\w\-]+")
_YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com"}
_SHORT_HOSTS = {"youtu.be", "www.youtu.be"}
# Paths that end in the video ID: /shorts/ID, /live/ID, /embed/ID.
_ID_PATH = re.compile(r"/(?:shorts|live|embed)/[\w\-]+/?")


def is_youtube_url(url: str) -> bool:
    """Return True when `url` looks like a YouTube video URL.

    Accepts the links people copy from browsers and the share menu: extra query
    parameters (`&t=42s`, `&list=...`, `?si=...`), `v` not being the first
    parameter, the mobile site, Shorts, live streams and embeds.
    """
    parts = urlsplit(url if "://" in url else "https://" + url)
    if parts.scheme not in ("http", "https"):
        return False
    # The exact host, as the transcript loader also matches it, so every URL accepted here loads.
    host = parts.netloc
    if host in _SHORT_HOSTS:
        return _VIDEO_ID.fullmatch(parts.path.strip("/")) is not None
    if host not in _YOUTUBE_HOSTS:
        return False
    if parts.path.rstrip("/") == "/watch":
        video_ids = parse_qs(parts.query).get("v", [])
        return len(video_ids) == 1 and _VIDEO_ID.fullmatch(video_ids[0]) is not None
    return _ID_PATH.fullmatch(parts.path) is not None


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
