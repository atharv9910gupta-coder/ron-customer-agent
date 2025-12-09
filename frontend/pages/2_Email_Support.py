# frontend/pages/2_Email_Support.py
import streamlit as st
from modules import groq_client

def app():
    st.header("Email Composer")
    to = st.text_input("To email")
    subject = st.text_input("Subject")
    body = st.text_area("Draft / Notes")
    if st.button("Generate Email"):
        prompt = f"Write a professional customer support email for subject: {subject}. Notes: {body}"
        messages = [{"role":"system", "content":"Write a short professional support email."}, {"role":"user", "content": prompt}]
        out = groq_client.run_groq_chat(messages)
        if "error" in out:
            st.error(out["error"])
        else:
            st.code(out["text"])
            st.session_state.generated_email = out["text"]
    if st.button("Send (backend)"):
        st.warning("Send uses backend API; implement backend endpoint for SMTP.")

