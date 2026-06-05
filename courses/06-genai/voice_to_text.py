"""
Voice to text scaffold using OpenAI Whisper API.
Useful for transcribing elder stories, field interviews, and call recordings.

Usage:
  OPENAI_API_KEY=... python voice_to_text.py path/to/audio.mp3

Author: Adrian Dunkley
"""

import os
import sys


def transcribe(path: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "Set OPENAI_API_KEY to transcribe."
    from openai import OpenAI
    client = OpenAI()
    with open(path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            prompt="Caribbean English. Common place names: Kingston, Bridgetown, Castries, Port of Spain.",
        )
    return resp.text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python voice_to_text.py path/to/audio.mp3")
        raise SystemExit(1)
    print(transcribe(sys.argv[1]))
