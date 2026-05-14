"""Minimal example: summarize a YouTube video with the OpenAI backend.

Run:
    OPENAI_API_KEY=... uv run python examples/summarize_youtube.py
"""

from __future__ import annotations

from websum import OpenAIBackend, Summarizer


def main() -> None:
    summarizer = Summarizer(backend=OpenAIBackend(model="gpt-4o-mini"))
    text = summarizer.summarize("https://www.youtube.com/watch?v=4pOpQwiUVXc")
    print(text)


if __name__ == "__main__":
    main()
