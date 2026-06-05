"""
Generate CSEC style practice questions from a topic, using an LLM if available,
or canned templates as a fallback.

Author: Adrian Dunkley
"""

import os
import sys


SYSTEM = (
    "You are a CSEC examiner. Generate three practice questions for the given topic. "
    "For each question include: a stem, four multiple choice options, the correct answer letter, "
    "and a one sentence explanation. Output JSON list."
)


def generate(topic: str) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            system=SYSTEM,
            messages=[{"role": "user", "content": f"Topic: {topic}"}],
        )
        return resp.content[0].text
    return """[
  {"stem": "Who led the Morant Bay Rebellion?", "options": ["A) Marcus Garvey", "B) Paul Bogle", "C) Nanny", "D) Sam Sharpe"], "answer": "B", "explanation": "Paul Bogle led the 1865 uprising in Saint Thomas, Jamaica."}
]"""


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or "Caribbean History, the Morant Bay Rebellion"
    print(generate(topic))
