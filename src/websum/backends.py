"""Pluggable LLM backends.

The library does not import any LLM SDK at top level. Backends are constructed
lazily so users only pay for the dependency they install (via the `ollama` or
`openai` extras).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from .exceptions import BackendNotAvailableError

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


BackendName = Literal["ollama", "openai"]


@runtime_checkable
class LLMBackend(Protocol):
    """Protocol for LLM backends.

    Any object exposing `build()` that returns a LangChain `BaseChatModel`
    can be used as a backend.
    """

    def build(self) -> BaseChatModel: ...


@dataclass(frozen=True)
class OllamaBackend:
    """Ollama backend configuration.

    Requires the `ollama` extra: `pip install websum[ollama]`.
    """

    model: str = "llama3:instruct"
    base_url: str = "http://127.0.0.1:11434"
    temperature: float = 0.0

    def build(self) -> BaseChatModel:
        try:
            from langchain_ollama import ChatOllama
        except ImportError as exc:
            raise BackendNotAvailableError(
                "Ollama backend requires `langchain-ollama`. "
                "Install with: pip install 'websum[ollama]'"
            ) from exc
        return ChatOllama(
            model=self.model,
            base_url=self.base_url,
            temperature=self.temperature,
        )


@dataclass(frozen=True)
class OpenAIBackend:
    """OpenAI backend configuration.

    Requires the `openai` extra: `pip install websum[openai]`.
    The OPENAI_API_KEY environment variable must be set unless `api_key` is provided.
    """

    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    api_key: str | None = None
    base_url: str | None = None

    def build(self) -> BaseChatModel:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise BackendNotAvailableError(
                "OpenAI backend requires `langchain-openai`. "
                "Install with: pip install 'websum[openai]'"
            ) from exc
        kwargs: dict[str, object] = {
            "model": self.model,
            "temperature": self.temperature,
        }
        if self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if self.base_url is not None:
            kwargs["base_url"] = self.base_url
        return ChatOpenAI(**kwargs)  # type: ignore[arg-type]


@dataclass(frozen=True)
class BackendRegistry:
    """Registry mapping backend names to default factories."""

    _factories: dict[str, type[LLMBackend]] = field(
        default_factory=lambda: {
            "ollama": OllamaBackend,
            "openai": OpenAIBackend,
        }
    )

    def create(self, name: BackendName, **kwargs: object) -> LLMBackend:
        if name not in self._factories:
            available = ", ".join(sorted(self._factories))
            raise ValueError(f"Unknown backend '{name}'. Available: {available}")
        factory = self._factories[name]
        return factory(**kwargs)


default_registry = BackendRegistry()
