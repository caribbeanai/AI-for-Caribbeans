"""
Streamlit starter for a Caribbean themed GenAI app.
Run with: streamlit run streamlit_app_skeleton.py

Author: Adrian Dunkley
"""

import os

try:
    import streamlit as st
except ImportError:
    raise SystemExit("Install streamlit. pip install streamlit")


SYSTEM = (
    "You are an assistant for small Caribbean businesses. "
    "Answer briefly, in plain English. When you do not know, say so."
)


def call_llm(history, user_msg):
    history = history + [{"role": "user", "content": user_msg}]
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=SYSTEM,
            messages=history,
        )
        return resp.content[0].text
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM}, *history],
        )
        return resp.choices[0].message.content
    return "Set ANTHROPIC_API_KEY or OPENAI_API_KEY in the environment."


def main():
    st.set_page_config(page_title="AI for Caribbeans", page_icon="🌴")
    st.title("AI for Caribbeans")
    st.caption("By Adrian Dunkley, the AI Boss.")

    if "history" not in st.session_state:
        st.session_state.history = []

    for m in st.session_state.history:
        st.chat_message(m["role"]).write(m["content"])

    user_msg = st.chat_input("Ask anything...")
    if user_msg:
        st.chat_message("user").write(user_msg)
        reply = call_llm(st.session_state.history, user_msg)
        st.chat_message("assistant").write(reply)
        st.session_state.history.extend([
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": reply},
        ])


if __name__ == "__main__":
    main()
