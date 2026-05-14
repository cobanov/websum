"""Minimal example: summarize a web page with the Ollama backend.

Run:
    uv run python examples/summarize_web.py
"""

from __future__ import annotations

from websum import OllamaBackend, Summarizer


def main() -> None:
    summarizer = Summarizer(backend=OllamaBackend(model="llama3:instruct"))
    text = summarizer.summarize("https://cobanov.dev/haftalik-bulten/hafta-13")
    print(text)


if __name__ == "__main__":
    main()
