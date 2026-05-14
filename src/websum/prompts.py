"""Prompt templates used by the summarization and translation chains."""

from __future__ import annotations

from langchain_core.prompts import PromptTemplate

WEB_SUMMARY_PROMPT = PromptTemplate(
    template="""As a professional summarizer, create a detailed and comprehensive summary of the provided text, be it an article, post, conversation, or passage, while adhering to these guidelines:

1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity.
2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
3. Rely strictly on the provided text, without including external information.
4. Format the summary in paragraph form for easy understanding.

By following this prompt, you will generate an effective summary that encapsulates the essence of the given text in a clear, detailed, and reader-friendly manner. Output as markdown.

"{text}"

DETAILED SUMMARY:""",
    input_variables=["text"],
)


YOUTUBE_SUMMARY_PROMPT = PromptTemplate(
    template="""As a professional summarizer specialized in video content, create a detailed and comprehensive summary of the YouTube video transcript provided. Adhere to these guidelines:

1. Capture the essence of the video, focusing on main ideas and key details. Ensure the summary is in-depth and insightful, reflecting any narrative or instructional elements present in the video.
2. Exclude any redundant expressions and non-critical details to enhance clarity and conciseness.
3. Base the summary strictly on the transcript provided, avoiding assumptions or additions from external sources.
4. Present the summary in well-structured paragraph form, making it easy to read and understand.

"{text}"

DETAILED SUMMARY:""",
    input_variables=["text"],
)


TRANSLATION_PROMPT = PromptTemplate(
    template="""As a professional translator, provide a detailed and comprehensive translation of the provided text into {target_language}, ensuring that the translation is accurate, coherent, and faithful to the original text.

"{text}"

DETAILED TRANSLATION:""",
    input_variables=["text", "target_language"],
)
