"""Tests for URL detection and loaders."""

from __future__ import annotations

import pytest

from websum import (
    InvalidURLError,
    TranscriptUnavailableError,
    is_youtube_url,
    load_youtube_transcript,
)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtube.com/watch?v=abc-123",
        "https://youtu.be/dQw4w9WgXcQ",
        "youtu.be/dQw4w9WgXcQ",
        # Links as browsers and the share menu copy them.
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLabc&index=2",
        "https://www.youtube.com/watch?feature=share&v=dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ?si=abc123",
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://www.youtube.com/live/dQw4w9WgXcQ?si=abc123",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
    ],
)
def test_is_youtube_url_true(url: str) -> None:
    assert is_youtube_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "https://youtube.com/playlist?list=abc",
        "https://www.youtube.com/@channel",
        "https://www.youtube.com/watch",
        "https://www.youtube.com/watch?list=PLabc",
        "https://youtu.be/",
        "https://notyoutube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com.example.com/watch?v=dQw4w9WgXcQ",
        "ftp://youtube.com/watch?v=dQw4w9WgXcQ",
        "not a url",
        "",
    ],
)
def test_is_youtube_url_false(url: str) -> None:
    assert not is_youtube_url(url)


def test_load_youtube_transcript_rejects_non_youtube_url() -> None:
    with pytest.raises(InvalidURLError):
        load_youtube_transcript("https://example.com")


def test_load_youtube_transcript_adds_missing_scheme(monkeypatch: pytest.MonkeyPatch) -> None:
    from langchain_community.document_loaders import YoutubeLoader

    seen = []

    def fake(url: str, **kwargs: object) -> object:
        seen.append(YoutubeLoader.extract_video_id(url))
        raise RuntimeError("stop before the network")

    monkeypatch.setattr(YoutubeLoader, "from_youtube_url", staticmethod(fake))
    for url in ("youtu.be/dQw4w9WgXcQ", "www.youtube.com/shorts/dQw4w9WgXcQ"):
        with pytest.raises(TranscriptUnavailableError):
            load_youtube_transcript(url)
    assert seen == ["dQw4w9WgXcQ", "dQw4w9WgXcQ"]
