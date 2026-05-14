"""Command-line interface for websum.

Usage:
    websum summarize URL [--backend ollama] [--model llama3:instruct]
    websum translate "text" [--target-language Turkish]
    websum ui [--host 0.0.0.0] [--port 7860]
"""

from __future__ import annotations

import logging
import sys
from typing import Annotated

import typer

from .__version__ import __version__
from .backends import LLMBackend, OllamaBackend, OpenAIBackend
from .exceptions import WebsumError
from .summarizer import Summarizer

app = typer.Typer(
    name="websum",
    help="Summarize web pages and YouTube videos with pluggable LLM backends.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"websum {__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable debug logging."),
    ] = False,
) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _build_backend(
    backend: str,
    model: str | None,
    base_url: str | None,
) -> LLMBackend:
    if backend == "ollama":
        return OllamaBackend(
            model=model or "llama3:instruct",
            base_url=base_url or "http://127.0.0.1:11434",
        )
    if backend == "openai":
        return OpenAIBackend(
            model=model or "gpt-4o-mini",
            base_url=base_url,
        )
    raise typer.BadParameter(f"Unknown backend: {backend}. Choose 'ollama' or 'openai'.")


@app.command()
def summarize(
    url: Annotated[str, typer.Argument(help="URL to summarize (web page or YouTube).")],
    backend: Annotated[
        str, typer.Option("--backend", "-b", help="LLM backend: ollama|openai.")
    ] = "ollama",
    model: Annotated[str | None, typer.Option("--model", "-m", help="Model name.")] = None,
    base_url: Annotated[
        str | None, typer.Option("--base-url", help="LLM endpoint base URL.")
    ] = None,
) -> None:
    """Summarize a URL (auto-detects web page vs. YouTube)."""
    try:
        llm = _build_backend(backend, model, base_url)
        summarizer = Summarizer(backend=llm)
        result = summarizer.summarize(url)
    except WebsumError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(result)


@app.command()
def translate(
    text: Annotated[str, typer.Argument(help="Text to translate (or '-' for stdin).")],
    target_language: Annotated[
        str, typer.Option("--target-language", "-t", help="Target language.")
    ] = "Turkish",
    backend: Annotated[str, typer.Option("--backend", "-b")] = "ollama",
    model: Annotated[str | None, typer.Option("--model", "-m")] = None,
    base_url: Annotated[str | None, typer.Option("--base-url")] = None,
) -> None:
    """Translate text into the target language."""
    if text == "-":
        text = sys.stdin.read()
    try:
        llm = _build_backend(backend, model, base_url)
        summarizer = Summarizer(backend=llm)
        result = summarizer.translate(text, target_language=target_language)
    except WebsumError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(result)


@app.command()
def ui(
    host: Annotated[str, typer.Option("--host", help="Server host.")] = "0.0.0.0",
    port: Annotated[int, typer.Option("--port", "-p", help="Server port.")] = 7860,
    backend: Annotated[str, typer.Option("--backend", "-b")] = "ollama",
    model: Annotated[str | None, typer.Option("--model", "-m")] = None,
    base_url: Annotated[str | None, typer.Option("--base-url")] = None,
) -> None:
    """Launch the Gradio web UI. Requires the `ui` extra."""
    try:
        from .webui import launch
    except ImportError as exc:
        typer.echo(
            "The Gradio UI requires the `ui` extra. Install with: pip install 'websum[ui]'",
            err=True,
        )
        raise typer.Exit(code=1) from exc
    llm = _build_backend(backend, model, base_url)
    launch(backend=llm, host=host, port=port)


if __name__ == "__main__":
    app()
