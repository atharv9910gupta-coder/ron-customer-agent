# frontend/pages/3_Tickets.py
import streamlit as st
from modules import db

def app():
    st.header("Tickets")
    tickets = db.get_tickets(200)
    if not tickets:
        st.info("No tickets yet.")
    for t in tickets:
        st.markdown("---")
        st.write(f"**{t['id']} — {t['title']}**")
        st.write(t['description'])
        st.write(f"Status: {t.get('status','open')}")

