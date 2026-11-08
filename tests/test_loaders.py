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
