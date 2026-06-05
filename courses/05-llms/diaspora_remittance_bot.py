"""
Scenario: a small diaspora remittance support bot.
Skeleton uses a static policy snippet plus an LLM. Replace policy with a real RAG layer.

Author: Adrian Dunkley
"""

import os


POLICY = """
SunRemit policy summary:
- Send limit: USD 2,999 per transfer, USD 9,999 per month, KYC required.
- Channels: bank deposit (1 to 2 hours), cash pickup (15 minutes), wallet (instant).
- Fees: bank deposit USD 2.99, cash pickup USD 4.99, wallet USD 1.99.
- Supported destinations include Jamaica, Haiti, Dominican Republic, Guyana, Trinidad, Barbados, Saint Lucia.
- Reversal policy: free reversal up to 60 minutes after send, otherwise USD 5.
- Disputes: file at support@sunremit.example within 30 days.
"""

SYSTEM = (
    "You are a polite, accurate support agent for SunRemit. "
    "Use only the policy below. If the answer is not in the policy, say so and offer to escalate. "
    "Reply in 80 words or less. Mirror the user's language (English, Patois, Kreyol, Spanish) gently.\n\n"
    f"POLICY:\n{POLICY}"
)


def reply(user_msg: str) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )
        return resp.content[0].text
    return "Set ANTHROPIC_API_KEY to run the real bot."


if __name__ == "__main__":
    for msg in [
        "Hi, can I send USD 1500 to my mother in Kingston today?",
        "Wah di fee for cash pickup, mi need it quick.",
        "Bonjou, eske mwen ka voye lajan an Ayiti?",
    ]:
        print(f"User: {msg}\nBot: {reply(msg)}\n")
