import streamlit as st
from modules.groq_client import ask_groq

def app():
    st.title("💬 Chat Support — Agent")

    st.markdown("Ask anything and the AI support agent will reply instantly.")

    # Chat input
    user_input = st.text_input("Your message:")

    if user_input:
        with st.spinner("Thinking..."):
            reply = ask_groq(user_input)

        st.success("Agent Reply:")
        st.write(reply)
