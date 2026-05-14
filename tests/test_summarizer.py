"""Tests for the Summarizer class using a stub backend."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

from langchain_core.documents import Document

from websum import Summarizer

if TYPE_CHECKING:
    from .conftest import StubBackend


def test_summarize_web_uses_stub_backend(stub_backend: StubBackend) -> None:
    fake_docs = [Document(page_content="hello world")]
    with patch("websum.summarizer.load_web_document", return_value=fake_docs):
        summarizer = Summarizer(backend=stub_backend)
        result = summarizer.summarize("https://example.com")
    assert result == "STUB SUMMARY"


def test_summarize_routes_youtube_url(stub_backend: StubBackend) -> None:
    summarizer = Summarizer(backend=stub_backend)
    with (
        patch("websum.summarizer.is_youtube_url", return_value=True),
        patch.object(summarizer, "summarize_youtube", return_value="YT") as yt_mock,
    ):
        assert summarizer.summarize("https://youtu.be/abc") == "YT"
    yt_mock.assert_called_once()


def test_translate_returns_text(stub_backend: StubBackend) -> None:
    summarizer = Summarizer(backend=stub_backend)
    result = summarizer.translate("hello", target_language="Turkish")
    assert result == "STUB SUMMARY"
