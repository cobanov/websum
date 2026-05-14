# Contributing

Thanks for your interest in improving websum. This document covers the dev setup, common workflows, and PR guidelines.

## Dev setup

Requirements: Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/cobanov/websum
cd websum
uv sync --all-extras
uv run pre-commit install
```

## Common commands

```bash
uv run pytest                   # Run tests
uv run pytest -m "not network"  # Skip tests that need the network
uv run ruff check . --fix       # Lint and auto-fix
uv run ruff format .            # Format
uv run mypy src/websum          # Type check (strict mode)
uv build                        # Build wheel + sdist
```

## Project layout

```
src/websum/
    __init__.py        Public API (re-exports)
    backends.py        LLMBackend Protocol, OllamaBackend, OpenAIBackend
    cli.py             Typer CLI entry point
    exceptions.py      Domain exceptions
    loaders.py         Web + YouTube document loaders
    prompts.py         Prompt templates
    summarizer.py      Summarizer high-level API
    webui.py           Gradio UI (requires `ui` extra)
tests/                 Pytest suite
examples/              Runnable example scripts
```

## Adding a backend

Backends just need a `.build()` method that returns a LangChain `BaseChatModel`:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class MyBackend:
    model: str = "default-model"
    def build(self):
        from somewhere import SomeChatModel
        return SomeChatModel(model=self.model)
```

Add it to `BackendRegistry` if you want CLI support.

## Testing

- All new code should ship with tests.
- Default to unit tests with the `StubBackend` from `tests/conftest.py`.
- Tests that hit a live LLM or the network should be marked `@pytest.mark.integration` or `@pytest.mark.network`.

## PR checklist

- [ ] Tests added / updated.
- [ ] `uv run ruff check .` clean.
- [ ] `uv run mypy src/websum` clean.
- [ ] `uv run pytest` passes.
- [ ] CHANGELOG.md entry under `## [Unreleased]`.
- [ ] Breaking changes called out in the PR description.

## Release process (maintainers)

1. Bump version in `src/websum/__version__.py` and `pyproject.toml`.
2. Move the `Unreleased` block in CHANGELOG.md to a new dated version section.
3. Commit, tag `vX.Y.Z`, push tags.
4. The `release.yml` workflow builds and publishes to PyPI via trusted publishing.
5. Create a GitHub Release with the changelog excerpt.
