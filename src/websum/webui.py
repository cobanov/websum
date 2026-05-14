"""Gradio web UI. Requires the `ui` extra (`pip install websum[ui]`)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .backends import LLMBackend, OllamaBackend
from .exceptions import WebsumError
from .summarizer import Summarizer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def build_app(backend: LLMBackend | None = None):  # type: ignore[no-untyped-def]
    """Build the Gradio Blocks app. Returns the Blocks instance."""
    import gradio as gr

    summarizer = Summarizer(backend=backend or OllamaBackend())

    def _summarize(url: str) -> tuple[str, gr.Button]:
        if not url.strip():
            return "Please enter a URL.", gr.Button(visible=False)
        try:
            text = summarizer.summarize(url)
        except WebsumError as exc:
            return f"Error: {exc}", gr.Button(visible=False)
        return text, gr.Button("Translate", visible=True)

    def _translate(text: str) -> str:
        try:
            return summarizer.translate(text)
        except WebsumError as exc:
            return f"Error: {exc}"

    with gr.Blocks(title="websum") as demo:
        gr.Markdown("# websum\nEasily summarize any web page or YouTube video with a single click.")
        with gr.Row(), gr.Column():
            url = gr.Text(label="URL", placeholder="Enter URL here")
            btn_generate = gr.Button("Generate", variant="primary")
            summary = gr.Markdown(label="Summary")
            btn_translate = gr.Button(visible=False)

        gr.Examples(
            [
                "https://cobanov.dev/haftalik-bulten/hafta-13",
                "https://bawolf.substack.com/p/embeddings-are-a-good-starting-point",
                "https://www.youtube.com/watch?v=4pOpQwiUVXc",
            ],
            inputs=[url],
        )

        btn_generate.click(_summarize, inputs=[url], outputs=[summary, btn_translate])
        btn_translate.click(_translate, inputs=[summary], outputs=[summary])

    return demo


def launch(
    backend: LLMBackend | None = None,
    host: str = "0.0.0.0",
    port: int = 7860,
) -> None:
    """Launch the Gradio web UI."""
    demo = build_app(backend=backend)
    demo.launch(server_name=host, server_port=port)
