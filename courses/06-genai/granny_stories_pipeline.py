"""
Scenario: "Granny's Stories", a small elder story preservation pipeline.

Pipeline steps:
  1. Transcribe an audio file with Whisper.
  2. Clean up the transcript with an LLM, preserving dialect.
  3. Produce a short summary suitable for a printable card.

Run:
  OPENAI_API_KEY=... ANTHROPIC_API_KEY=... python courses/06-genai/granny_stories_pipeline.py path/to/audio.mp3

Author: Adrian Dunkley
"""

import os
import sys


CLEAN_SYSTEM = (
    "You receive a raw Whisper transcript of a Caribbean elder telling a story. "
    "Clean it up while preserving dialect words, names, and meaning. Do not standardise "
    "to British English. Break into paragraphs. Keep it warm and faithful."
)

SUMMARY_SYSTEM = (
    "You write short, dignified summaries of elder stories suitable for a printable card. "
    "Two short paragraphs. Highlight people, place, and the lesson without flattening the voice."
)


def transcribe(path: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "(set OPENAI_API_KEY to transcribe)"
    from openai import OpenAI
    client = OpenAI()
    with open(path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            prompt="Caribbean English and dialect. Common names of places: Kingston, Bridgetown, Castries, Port of Spain.",
        )
    return resp.text


def llm(system: str, user: str) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        client = Anthropic()
        r = client.messages.create(model="claude-sonnet-4-6", max_tokens=600,
                                   system=system, messages=[{"role": "user", "content": user}])
        return r.content[0].text
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI()
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return r.choices[0].message.content
    return "(set ANTHROPIC_API_KEY or OPENAI_API_KEY)"


def main():
    if len(sys.argv) < 2:
        print("Usage: python granny_stories_pipeline.py path/to/audio.mp3")
        return
    raw = transcribe(sys.argv[1])
    print("=== Raw transcript ===\n", raw)
    cleaned = llm(CLEAN_SYSTEM, raw)
    print("\n=== Cleaned ===\n", cleaned)
    summary = llm(SUMMARY_SYSTEM, cleaned)
    print("\n=== Summary card ===\n", summary)


if __name__ == "__main__":
    main()
