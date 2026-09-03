<p align="center">
  <strong>websum</strong><br>
  Summarise a web page or a YouTube video, with whichever model you want behind it.
</p>

<p align="center">
  <a href="https://pypi.org/project/websum/">PyPI</a> ·
  <a href="CHANGELOG.md">changelog</a> ·
  <a href="CONTRIBUTING.md">contributing</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/websum/"><img alt="pypi" src="https://img.shields.io/pypi/v/websum?color=5b8def&labelColor=1a1a1a"></a>
  <a href="https://pypi.org/project/websum/"><img alt="python" src="https://img.shields.io/pypi/pyversions/websum?color=5b8def&labelColor=1a1a1a"></a>
  <img alt="tests" src="https://img.shields.io/badge/tests-19-5b8def?labelColor=1a1a1a">
  <a href="https://github.com/cobanov/websum/actions/workflows/ci.yml"><img alt="ci" src="https://github.com/cobanov/websum/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="licence" src="https://img.shields.io/badge/licence-MIT-5b8def?labelColor=1a1a1a"></a>
</p>

---

Summarising a page is a few lines of LangChain right up until you want the same call
to also take a YouTube link, chunk a transcript that will not fit in a context
window, run against a local Ollama on a laptop with no network, and then move to
OpenAI without any of the calling code changing. That is the part this packages.

One object, `Summarizer`, takes a URL and works out whether it is a page or a video.
The model behind it is a constructor argument, so swapping Ollama for OpenAI, or for
something you wrote yourself, is a single line.

```python
from websum import Summarizer, OllamaBackend

s = Summarizer(backend=OllamaBackend(model="llama3:instruct"))
print(s.summarize("https://www.youtube.com/watch?v=4pOpQwiUVXc"))
```

- **Pages and YouTube through the same call.** `summarize(url)` detects which it has.
  `summarize_web` and `summarize_youtube` are there when you already know.
- **The backend is a Protocol**, not a base class to inherit. Anything with a
  `.build()` returning a LangChain chat model satisfies it.
- **Local by default.** Ollama is a first-class backend, so nothing has to leave the
  machine, and no key is required to try it.
- **Long inputs are chunked**, so a two-hour transcript does not have to fit anywhere
  in one piece.
- **A CLI, a library and a Gradio UI** over the same code, and a `py.typed` marker so
  the API type-checks downstream.

## Install

```bash
pip install 'websum[ollama]'     # library + CLI, local models
pip install 'websum[openai]'     # OpenAI backend
pip install 'websum[ui,ollama]'  # with the Gradio web UI
pip install 'websum[all]'        # everything
```

Using `uv`:

```bash
uv add 'websum[ollama]'
```

Python 3.10 to 3.13. The base install carries no model client at all, which is why
the backend is an extra: installing `websum` alone should not drag in an SDK you are
not going to call.

## Use

**As a library**

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

**From the shell**

```bash
websum summarize https://example.com
websum summarize https://example.com --backend openai --model gpt-4o-mini
websum translate "Hello world" --target-language Turkish
websum ui --port 7860
```

`websum --help` has the full reference.

**In a browser**

```bash
websum ui --port 7860
```

<p align="center">
  <img src="assets/gradio.png" alt="The Gradio UI with a URL box and the summary below it" width="560">
</p>

## The API

| Object | Purpose |
| --- | --- |
| `Summarizer` | The high-level API. `summarize(url)`, `summarize_web(url)`, `summarize_youtube(url)`, `translate(text)` |
| `SummarizerConfig` | Chunking and language settings |
| `OllamaBackend`, `OpenAIBackend` | The built-in backends. Frozen dataclasses with `.build()` |
| `LLMBackend` (Protocol) | Implement this to plug in anything else |
| `BackendRegistry` | Maps string names to backend classes, which is how the CLI resolves `--backend` |

Every public name is re-exported from the top-level `websum` package and listed in
`__all__`.

### Writing a backend

`LLMBackend` is a `Protocol`, so there is nothing to subclass and nothing to
register. A class with a `build()` method already satisfies it:

```python
from dataclasses import dataclass
from websum import LLMBackend, Summarizer

@dataclass
class MyBackend:
    def build(self):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-sonnet-5")

assert isinstance(MyBackend(), LLMBackend)  # runtime Protocol check
s = Summarizer(backend=MyBackend())
```

The import lives inside `build()` on purpose: a backend that is never constructed
should not cost an import of an SDK that may not be installed.

## Docker

```bash
docker build -t websum .
docker run -p 7860:7860 websum

# when ollama is running on the host
docker run --network host -p 7860:7860 websum
```

The image starts `websum ui` by default.

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

CI runs the 19 tests on 3.10, 3.11, 3.12 and 3.13, with `ruff`, `ruff format --check`
and `mypy` on top. `pytest-randomly` shuffles the order every run, so a test that
only passes because another one ran first fails here rather than later.
[CONTRIBUTING.md](CONTRIBUTING.md) has the full guide.

## Upgrading from 0.1.x

The 0.1.x scripts under `app/` are gone. Everything moved into the `websum` package
behind a typed, importable API.

| Before | After |
| --- | --- |
| `python app/summarizer.py -u URL` | `websum summarize URL` |
| `python app/webui.py` | `websum ui` |
| `from summarizer import setup_summarization_chain` | `from websum import Summarizer` |
| Hardcoded `ChatOllama` | `OllamaBackend`, `OpenAIBackend`, or your own `LLMBackend` |
| `pip install -r requirements.txt` | `pip install 'websum[ollama]'` |

## Licence

MIT. See [LICENSE](LICENSE).
