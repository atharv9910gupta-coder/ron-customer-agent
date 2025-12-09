import streamlit as st
from modules import groq_client, db

st.header("Chat Support — Agent")

tickets = db.get_tickets(50)
ticket_map = {f"{t['id']} — {t['title']}": t for t in tickets}

choice = st.selectbox("Open ticket", ["Create new"] + list(ticket_map.keys()))

if choice == "Create new":
    title = st.text_input("Ticket Title")
    desc = st.text_area("Description")

    if st.button("Create ticket"):
        new = db.create_ticket(title, desc)
        st.success(f"Created ticket {new.get('id')}")
        st.experimental_rerun()

else:
    ticket = ticket_map[choice]
    st.subheader(ticket["title"])
    st.write(ticket["description"])

    user_msg = st.text_input("Agent reply:")

    if st.button("Send reply"):
        db.append_message(ticket["id"], "agent", user_msg)
        st.success("Reply saved.")
        st.experimental_rerun()

    res = db.supabase.table("messages").select("*") \
        .eq("ticket_id", ticket["id"]) \
        .order("created_at", desc=True).execute()

    if res.status_code == 200:
        for m in reversed(res.data):
            st.markdown(f"**{m['role']}:** {m['content']}")

