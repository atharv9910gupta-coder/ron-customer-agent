# frontend/app.py
import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="RON — Premium Agent", layout="wide", initial_sidebar_state="expanded")

# safe logo load
logo = None
logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    try:
        logo = Image.open(logo_path)
    except Exception:
        logo = None

with st.sidebar:
    if logo:
        st.image(logo, width=100)
    st.title("RON System")
    st.markdown("Enterprise AI support — demo")

st.title("RON — Premium Customer Support Platform")
st.markdown("Use the left sidebar to open pages: Chat Support, Email Support, Tickets, Settings.")
