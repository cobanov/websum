# websum

[![CI](https://github.com/cobanov/websum/actions/workflows/ci.yml/badge.svg)](https://github.com/cobanov/websum/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/websum.svg)](https://pypi.org/project/websum/)
[![PyPI](https://img.shields.io/pypi/v/websum.svg)](https://pypi.org/project/websum/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Summarize web pages and YouTube videos with pluggable LLM backends. Ships with first-class support for **Ollama** (local) and **OpenAI**, plus an optional Gradio web UI.

## Installation

```bash
# Library + CLI, with Ollama backend
pip install 'websum[ollama]'

# With OpenAI backend
pip install 'websum[openai]'

# With the Gradio web UI
pip install 'websum[ui,ollama]'

# Everything
pip install 'websum[all]'
```

Using `uv`:

```bash
uv add 'websum[ollama]'
```

## Quickstart

### Library

```python
from websum import Summarizer, OllamaBackend

s = Summarizer(backend=OllamaBackend(model="llama3:instruct"))
print(s.summarize("https://cobanov.dev/haftalik-bulten/hafta-13"))
print(s.summarize("https://www.youtube.com/watch?v=4pOpQwiUVXc"))
print(s.translate("Hello world", target_language="Turkish"))
```

Swap the backend without touching anything else:

```python
from websum import Summarizer, OpenAIBackend

s = Summarizer(backend=OpenAIBackend(model="gpt-4o-mini"))
```

### CLI

```bash
# Summarize a web page or YouTube URL (auto-detected)
websum summarize https://example.com

# Use OpenAI instead of Ollama
websum summarize https://example.com --backend openai --model gpt-4o-mini

# Translate
websum translate "Hello world" --target-language Turkish

# Launch the Gradio UI
websum ui --port 7860
```

Run `websum --help` for the full command reference.

## API overview

| Object | Purpose |
| --- | --- |
| `Summarizer` | High-level API. `summarize(url)`, `summarize_web(url)`, `summarize_youtube(url)`, `translate(text)`. |
| `SummarizerConfig` | Chunking and language settings. |
| `OllamaBackend`, `OpenAIBackend` | Built-in backends. Frozen dataclasses with `.build()`. |
| `LLMBackend` (Protocol) | Implement this to plug in any backend. |
| `BackendRegistry` | Map string names to backend classes (used by the CLI). |

All public names are re-exported from the top-level `websum` package and listed in `__all__`.

## Custom backends

```python
from dataclasses import dataclass
from websum import LLMBackend, Summarizer

@dataclass
class MyBackend:
    def build(self):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-3-5-sonnet-latest")

assert isinstance(MyBackend(), LLMBackend)  # Protocol check
s = Summarizer(backend=MyBackend())
```

## Docker

```bash
docker build -t websum .
docker run -p 7860:7860 websum

# Run when ollama is on the host
docker run --network host -p 7860:7860 websum
```

The image starts `websum ui` by default.

## Migration from 0.1.x

The 0.1.x scripts under `app/` (`summarizer.py`, `translator.py`, `yt_summarizer.py`, `webui.py`) are gone. Everything moved into the `websum` package with a typed, importable API.

| Before | After |
| --- | --- |
| `python app/summarizer.py -u URL` | `websum summarize URL` |
| `python app/webui.py` | `websum ui` |
| `from summarizer import setup_summarization_chain` | `from websum import Summarizer` |
| Hardcoded `ChatOllama` | `OllamaBackend` / `OpenAIBackend` / custom `LLMBackend` |
| `pip install -r requirements.txt` | `pip install 'websum[ollama]'` |

## Development

```bash
git clone https://github.com/cobanov/websum
cd websum
uv sync --all-extras
uv run pre-commit install
uv run pytest
uv run ruff check .
uv run mypy src/websum
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## License

MIT. See [LICENSE](LICENSE).
