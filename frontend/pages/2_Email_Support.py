# frontend/pages/2_Email_Support.py
import streamlit as st
from modules import groq_client, tools

st.header("✉️ Email Support")

to_email = st.text_input("To (email)")
subject = st.text_input("Subject")
notes = st.text_area("Notes (context for the AI)")

if st.button("Generate email"):
    prompt = f"Write a professional support email.\nSubject: {subject}\nContext: {notes}"
    messages = [{"role":"system","content":"You are a professional email writer."}, {"role":"user","content":prompt}]
    out = groq_client.run_groq_chat(messages)
    if "error" in out:
        st.error(out["error"])
    else:
        st.session_state.generated_email = out.get("text","")
        st.success("Generated email ready.")

if "generated_email" in st.session_state:
    st.subheader("Generated Email")
    st.write(st.session_state.generated_email)

if st.button("Send email (placeholder)"):
    res = tools.send_email_placeholder(to_email, subject, st.session_state.get("generated_email",""))
    if res.get("ok"):
        st.success("Email sent via backend.")
    else:
        st.error(res.get("error","Not configured"))
