# frontend/pages/5_Settings.py
import streamlit as st, os

def app():
    st.header("Settings & Secrets")
    st.write("Add keys into your deployment environment — Do not store keys in the repo.")
    groq = os.getenv("GROQ_API_KEY")
    sup_url = os.getenv("SUPABASE_URL")
    if groq:
        st.success("GROQ key found")
    else:
        st.warning("GROQ key missing")
    if sup_url:
        st.success("Supabase URL found")
    else:
        st.warning("Supabase URL missing")

