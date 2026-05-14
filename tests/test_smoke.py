"""Smoke tests: ensure the package imports and exposes its public API."""

from __future__ import annotations


def test_package_imports() -> None:
    import websum

    assert websum.__version__


def test_public_api_exports() -> None:
    import websum

    for name in [
        "Summarizer",
        "SummarizerConfig",
        "OllamaBackend",
        "OpenAIBackend",
        "LLMBackend",
        "BackendRegistry",
        "default_registry",
        "is_youtube_url",
        "load_web_document",
        "load_youtube_transcript",
        "WebsumError",
        "BackendNotAvailableError",
        "InvalidURLError",
        "DocumentLoadError",
        "TranscriptUnavailableError",
    ]:
        assert hasattr(websum, name), f"Missing public export: {name}"


def test_py_typed_marker_present() -> None:
    import importlib.resources

    files = importlib.resources.files("websum")
    assert (files / "py.typed").is_file()
