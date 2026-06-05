"""
A starter for a WhatsApp customer support bot using the WhatsApp Cloud API
plus an LLM. This file is the core handler. You provide a webhook server
(Flask or FastAPI) and your WhatsApp Business credentials.

Author: Adrian Dunkley
"""

import os


SYSTEM = (
    "You are the customer support assistant for a small Caribbean business. "
    "Be warm, direct, and helpful. If you cannot answer, say so and offer "
    "to pass the message to a human team member. Keep replies under 60 words."
)


def handle_message(text: str, history: list[dict] | None = None) -> str:
    history = history or []
    history = history + [{"role": "user", "content": text}]
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=SYSTEM,
            messages=history,
        )
        return resp.content[0].text
    return "Thanks for reaching out. Our team will get back to you shortly."


if __name__ == "__main__":
    samples = [
        "Hi, do you ship to Tobago?",
        "I sent payment yesterday, when will I get my order?",
        "Wah time allyuh open today?",
    ]
    for s in samples:
        print(f"Customer: {s}\nBot: {handle_message(s)}\n")
