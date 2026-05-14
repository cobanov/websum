"""High-level summarization and translation API.

This module exposes the public `Summarizer` class plus convenience functions.
Backends are pluggable through the `LLMBackend` Protocol.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .backends import LLMBackend, OllamaBackend
from .loaders import is_youtube_url, load_web_document, load_youtube_transcript
from .prompts import TRANSLATION_PROMPT, WEB_SUMMARY_PROMPT, YOUTUBE_SUMMARY_PROMPT

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger = logging.getLogger(__name__)


@dataclass
class SummarizerConfig:
    """Configuration for `Summarizer`."""

    chunk_size: int = 7500
    chunk_overlap: int = 100
    youtube_languages: tuple[str, ...] = ("en", "en-US")


@dataclass
class Summarizer:
    """Summarize web pages and YouTube videos.

    Example:
        >>> from websum import Summarizer, OllamaBackend
        >>> s = Summarizer(backend=OllamaBackend(model="llama3:instruct"))
        >>> text = s.summarize("https://example.com")
    """

    backend: LLMBackend = field(default_factory=OllamaBackend)
    config: SummarizerConfig = field(default_factory=SummarizerConfig)

    def summarize(self, url: str) -> str:
        """Summarize a URL. Auto-detects YouTube vs. web page.

        Raises:
            InvalidURLError: if URL format is invalid.
            DocumentLoadError: if the document cannot be loaded.
        """
        if is_youtube_url(url):
            return self.summarize_youtube(url)
        return self.summarize_web(url)

    def summarize_web(self, url: str) -> str:
        """Summarize a web page URL."""
        docs = load_web_document(url)
        return self._summarize_simple(docs)

    def summarize_youtube(self, url: str) -> str:
        """Summarize a YouTube video URL using its transcript."""
        transcript = load_youtube_transcript(url, self.config.youtube_languages)
        chunks = self._split(transcript)
        return self._summarize_mapreduce(chunks)

    def translate(self, text: str, target_language: str = "Turkish") -> str:
        """Translate `text` into `target_language`."""
        llm = self.backend.build()
        chain = TRANSLATION_PROMPT | llm
        result = chain.invoke({"text": text, "target_language": target_language})
        return _extract_text(result)

    def _summarize_simple(self, docs: list[Document]) -> str:
        llm = self.backend.build()
        chain = WEB_SUMMARY_PROMPT | llm
        joined = "\n\n".join(doc.page_content for doc in docs)
        result = chain.invoke({"text": joined})
        return _extract_text(result)

    def _summarize_mapreduce(self, chunks: list[Document]) -> str:
        from langchain.chains.summarize import load_summarize_chain

        llm = self.backend.build()
        chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            map_prompt=YOUTUBE_SUMMARY_PROMPT,
            combine_prompt=YOUTUBE_SUMMARY_PROMPT,
        )
        result = chain.invoke({"input_documents": chunks})
        if isinstance(result, dict):
            return str(result.get("output_text", result))
        return str(result)

    def _split(self, docs: list[Document]) -> list[Document]:
        from langchain_text_splitters import TokenTextSplitter

        splitter = TokenTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        return splitter.split_documents(docs)


def _extract_text(result: object) -> str:
    """Extract the textual content from a LangChain chat result."""
    content = getattr(result, "content", result)
    return str(content)
