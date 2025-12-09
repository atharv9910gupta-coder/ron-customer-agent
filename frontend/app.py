# frontend/app.py - main landing page (Streamlit)
import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="RON — Premium Agent", page_icon="assets/logo.png", layout="wide")

# header + logo
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, width=100)
else:
    st.sidebar.title("RON")

st.sidebar.title("RON Admin")
st.sidebar.markdown("Enterprise AI support system")

# pages are auto-loaded from /pages
st.title("RON — Premium Customer Support Platform")
st.write("Use the left sidebar to navigate.")
st.write("This frontend uses Supabase for auth & DB, Groq for AI (llama-3.1-8b-instant).")

