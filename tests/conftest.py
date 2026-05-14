"""Shared pytest fixtures."""

from __future__ import annotations

from itertools import cycle
from typing import TYPE_CHECKING

import pytest
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


def _make_fake_chat_model(response: str = "STUB SUMMARY") -> GenericFakeChatModel:
    return GenericFakeChatModel(messages=cycle([AIMessage(content=response)]))


class StubBackend:
    """LLMBackend stub that returns a deterministic LangChain fake model."""

    def __init__(self, response: str = "STUB SUMMARY") -> None:
        self.response = response
        self._model = _make_fake_chat_model(response)

    def build(self) -> BaseChatModel:
        return self._model


@pytest.fixture
def stub_backend() -> StubBackend:
    return StubBackend()
