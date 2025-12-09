# frontend/pages/3_Tickets.py
import streamlit as st
from modules import db

st.header("🎫 Tickets")

tickets = db.list_tickets(200)
if not tickets:
    st.info("No tickets yet.")
for t in tickets:
    st.markdown("---")
    st.write(f"**{t.get('id', '?')} — {t.get('title','')}**")
    st.write(t.get("description",""))
    st.write(f"Status: {t.get('status','open')}")
