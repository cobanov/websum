# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-05-14

### Added
- Public `websum` package with typed, importable API (`Summarizer`, `SummarizerConfig`).
- Pluggable LLM backend system via `LLMBackend` Protocol; built-in `OllamaBackend` and `OpenAIBackend`.
- `BackendRegistry` for name-to-class lookup, used by the CLI.
- Domain-specific exceptions: `WebsumError`, `BackendNotAvailableError`, `InvalidURLError`, `DocumentLoadError`, `TranscriptUnavailableError`.
- Modern `typer`-based CLI with `summarize`, `translate`, and `ui` subcommands.
- `py.typed` marker for type checker consumers (PEP 561).
- `pyproject.toml` (PEP 621), `uv`-based workflow, `hatchling` build backend.
- Test suite (pytest) with smoke, loader, backend, summarizer, and CLI tests.
- GitHub Actions CI: lint (ruff), type-check (mypy strict), test matrix (3.10-3.13), build.
- GitHub Actions release workflow with PyPI trusted publishing.
- Pre-commit hooks (ruff, mypy, hygiene checks).
- `examples/` directory with runnable scripts.

### Changed
- **BREAKING**: Project renamed from `easy-web-summarizer` to `websum`. Import as `import websum`.
- **BREAKING**: Loose scripts under `app/` are gone. Use the `Summarizer` API or the `websum` CLI.
- **BREAKING**: CLI entry point changed from `python app/summarizer.py -u URL` to `websum summarize URL`.
- **BREAKING**: `webui.py` removed; launch via `websum ui` (requires the `ui` extra).
- Moved code to `src/websum/` layout.
- Ollama is now an optional extra (`websum[ollama]`), not a core dependency.
- Updated to `langchain>=0.3` (split-out packages: `langchain-ollama`, `langchain-openai`).
- Dockerfile rebuilt around `uv` and Python 3.12.

### Removed
- `setup.py`, `requirements.txt`, `MANIFEST.in` (replaced by `pyproject.toml`).
- Hardcoded `ChatOllama` instantiation in core modules.
- Top-level `app/` scripts.

## [0.1.0] - 2024 (initial)
- First public scripts under `app/` using LangChain + ChatOllama.
- Gradio UI, web page and YouTube summarization, Turkish translation.

[0.2.0]: https://github.com/mertcobanov/easy-web-summarizer/releases/tag/v0.2.0
