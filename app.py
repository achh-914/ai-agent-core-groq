import streamlit as st
from groq import Groq
import os
from config import GROQ_API_KEY, DEFAULT_MODEL

st.set_page_config(page_title="AI Agent Core", page_icon="🤖", layout="centered")

st.title("🤖 AI Agent Core (Groq Powered)")
st.caption("Powered by Groq Cloud Infrastructure & Terraform")

api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")

if not api_key:
    api_key = st.text_input("Enter your Groq API Key:", type="password")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful AI Assistant."}
        ]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
