# frontend/pages/4_Settings.py
import streamlit as st
import os

st.header("⚙ Settings")

st.write("Environment / secrets check:")

groq = os.getenv("GROQ_API_KEY")
sup_url = os.getenv("SUPABASE_URL")
if groq:
    st.success("GROQ_API_KEY detected")
else:
    st.warning("GROQ_API_KEY missing. Add in Streamlit Secrets or environment vars.")

if sup_url:
    st.success("SUPABASE_URL detected")
else:
    st.info("SUPABASE not configured — app will use local JSON fallback.")
