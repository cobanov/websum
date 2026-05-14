"""websum: pluggable LLM-powered summarization for web pages and YouTube videos."""

from __future__ import annotations

import logging

from .__version__ import __version__
from .backends import (
    BackendName,
    BackendRegistry,
    LLMBackend,
    OllamaBackend,
    OpenAIBackend,
    default_registry,
)
from .exceptions import (
    BackendNotAvailableError,
    DocumentLoadError,
    InvalidURLError,
    TranscriptUnavailableError,
    WebsumError,
)
from .loaders import (
    is_youtube_url,
    load_web_document,
    load_youtube_transcript,
)
from .summarizer import Summarizer, SummarizerConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "BackendName",
    "BackendNotAvailableError",
    "BackendRegistry",
    "DocumentLoadError",
    "InvalidURLError",
    "LLMBackend",
    "OllamaBackend",
    "OpenAIBackend",
    "Summarizer",
    "SummarizerConfig",
    "TranscriptUnavailableError",
    "WebsumError",
    "__version__",
    "default_registry",
    "is_youtube_url",
    "load_web_document",
    "load_youtube_transcript",
]
