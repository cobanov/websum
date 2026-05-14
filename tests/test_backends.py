"""Tests for backend registry and Protocol conformance."""

from __future__ import annotations

import pytest

from websum import LLMBackend, OllamaBackend, OpenAIBackend, default_registry


def test_ollama_backend_satisfies_protocol() -> None:
    backend = OllamaBackend()
    assert isinstance(backend, LLMBackend)


def test_openai_backend_satisfies_protocol() -> None:
    backend = OpenAIBackend()
    assert isinstance(backend, LLMBackend)


def test_registry_creates_ollama() -> None:
    backend = default_registry.create("ollama")
    assert isinstance(backend, OllamaBackend)


def test_registry_creates_openai() -> None:
    backend = default_registry.create("openai")
    assert isinstance(backend, OpenAIBackend)


def test_registry_unknown_backend_raises() -> None:
    with pytest.raises(ValueError, match="Unknown backend"):
        default_registry.create("nope")  # type: ignore[arg-type]


def test_ollama_backend_overrides() -> None:
    backend = OllamaBackend(model="llama3.1", base_url="http://localhost:1234")
    assert backend.model == "llama3.1"
    assert backend.base_url == "http://localhost:1234"
