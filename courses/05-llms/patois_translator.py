"""
Patois translator helper. Uses an LLM to map Jamaican Patois sentences
into Standard English and vice versa. Designed as a teaching example.

Usage:
  ANTHROPIC_API_KEY=... python patois_translator.py "Wah gwaan, everyting irie?"

Author: Adrian Dunkley
"""

import os
import sys


SYSTEM = (
    "You translate between Jamaican Patois and Standard English. "
    "Preserve tone and register. If the input is already in Standard English, "
    "produce a natural Patois rendering. Keep cultural references intact. "
    "Output only the translation, no commentary."
)


def translate(text: str) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=SYSTEM,
            messages=[{"role": "user", "content": text}],
        )
        return resp.content[0].text
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM},
                      {"role": "user", "content": text}],
        )
        return resp.choices[0].message.content
    return "(set ANTHROPIC_API_KEY or OPENAI_API_KEY to translate)"


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "Mi soon come, mek wi link up later."
    print(translate(text))
