import streamlit as st
from modules.db import db

def app():
    st.title("🎫 Ticket System")

    st.subheader("Create a new ticket")

    title = st.text_input("Ticket title")
    description = st.text_area("Description")

    if st.button("Create Ticket"):
        if title and description:
            db.create_ticket(title=title, description=description)
            st.success("Ticket created successfully!")
        else:
            st.error("Please fill all fields.")

    st.subheader("All Tickets")
    tickets = db.get_tickets(50)

    for t in tickets:
        st.write(f"**#{t['id']} — {t['title']}**")
        st.write(t["description"])
        st.markdown("---")
