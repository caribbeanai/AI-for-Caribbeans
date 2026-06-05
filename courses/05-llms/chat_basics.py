"""
Minimal chat client. Reads API keys from environment variables.
Set one of:
  ANTHROPIC_API_KEY
  OPENAI_API_KEY

Usage:
  python chat_basics.py "Tell me about Maroon history in Accompong, Jamaica."

Author: Adrian Dunkley
"""

import os
import sys


SYSTEM = (
    "You are a Caribbean knowledge assistant. Be direct, accurate, and warm. "
    "When you do not know, say so. Cite sources when possible."
)


def ask_claude(prompt: str) -> str:
    from anthropic import Anthropic
    client = Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def ask_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def main():
    prompt = " ".join(sys.argv[1:]) or "Give one fact about each Caribbean country."
    if os.getenv("ANTHROPIC_API_KEY"):
        print(ask_claude(prompt))
    elif os.getenv("OPENAI_API_KEY"):
        print(ask_openai(prompt))
    else:
        print("Set ANTHROPIC_API_KEY or OPENAI_API_KEY to run.")


if __name__ == "__main__":
    main()
