"""Tests for URL detection and loaders."""

from __future__ import annotations

import pytest

from websum import InvalidURLError, is_youtube_url, load_youtube_transcript


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtube.com/watch?v=abc-123",
        "https://youtu.be/dQw4w9WgXcQ",
        "youtu.be/dQw4w9WgXcQ",
    ],
)
def test_is_youtube_url_true(url: str) -> None:
    assert is_youtube_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "https://youtube.com/playlist?list=abc",
        "not a url",
        "",
    ],
)
def test_is_youtube_url_false(url: str) -> None:
    assert not is_youtube_url(url)


def test_load_youtube_transcript_rejects_non_youtube_url() -> None:
    with pytest.raises(InvalidURLError):
        load_youtube_transcript("https://example.com")
