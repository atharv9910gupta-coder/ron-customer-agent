# frontend/pages/4_Admin.py
import streamlit as st
from modules import db

def app():
    st.header("Admin Dashboard")
    st.write("Admin-only controls. Use backend service keys for sensitive actions.")
    # Example quick stats
    tickets = db.get_tickets(1000)
    st.metric("Open tickets", len([t for t in tickets if t.get("status","open") == "open"]))
    # Export sample
    if st.button("Export tickets (JSON)"):
        st.download_button("Download JSON", data=str(tickets), file_name="tickets.json")

