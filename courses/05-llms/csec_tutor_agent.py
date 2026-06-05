"""
A simple CSEC tutor agent that uses one tool: a lookup over a tiny topic bank.
This is an agent loop scaffold. Extend the tool set as you grow it.

Author: Adrian Dunkley
"""

import json
import os
from pathlib import Path


TOPIC_BANK = {
    "morant bay rebellion": "October 1865 uprising in Saint Thomas, Jamaica, led by Paul Bogle. George William Gordon executed. Led to direct British rule.",
    "haitian revolution": "1791 to 1804. Enslaved people led by Toussaint Louverture and Jean-Jacques Dessalines defeated French forces. First Black republic.",
    "federation": "West Indies Federation, 1958 to 1962. Aimed at political union of British Caribbean colonies. Dissolved after Jamaica withdrew.",
    "pythagoras": "In a right angled triangle, the square of the hypotenuse equals the sum of the squares of the other two sides. a^2 + b^2 = c^2.",
    "photosynthesis": "Plants convert light, water, and carbon dioxide into glucose and oxygen. 6 CO2 + 6 H2O -> C6H12O6 + 6 O2.",
}


def lookup_topic(name: str) -> str:
    """Look up a CSEC topic in the bank."""
    key = name.lower().strip()
    return TOPIC_BANK.get(key, f"Topic '{name}' not in the bank. Try adding it.")


def main():
    tool_schema = [{
        "name": "lookup_topic",
        "description": "Look up a CSEC topic and return a short factual summary.",
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    }]

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to run the full agent loop.")
        print("Showing tool response only for demo.")
        print(lookup_topic("morant bay rebellion"))
        return

    from anthropic import Anthropic
    client = Anthropic()
    messages = [{"role": "user", "content": "Explain the Morant Bay Rebellion for a CSEC student. Use the lookup tool."}]
    while True:
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            tools=tool_schema,
            messages=messages,
            system="You are a Caribbean CSEC tutor. Use tools when helpful. Be concise and accurate."
        )
        if resp.stop_reason == "tool_use":
            tool_use = [b for b in resp.content if b.type == "tool_use"][0]
            result = lookup_topic(**tool_use.input)
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({"role": "user", "content": [{
                "type": "tool_result", "tool_use_id": tool_use.id, "content": result,
            }]})
            continue
        print("".join(b.text for b in resp.content if b.type == "text"))
        return


if __name__ == "__main__":
    main()
