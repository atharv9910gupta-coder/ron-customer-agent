
# frontend/pages/1_Chat_Support.py
import streamlit as st
from modules import groq_client, db

def app():
    st.header("Chat Support — Agent")
    # ticket selection
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
            # append message to messages table
            db.append_message(ticket["id"], "agent", user_msg)
            st.success("Reply saved to ticket.")
            st.experimental_rerun()
        # show history
        res = st.button("Refresh messages")
        res = db.supabase.table("messages").select("*").eq("ticket_id", ticket["id"]).order("created_at", desc=True).execute()
        if res.status_code == 200:
            for m in reversed(res.data):
                role = m["role"]
                content = m["content"]
                st.markdown(f"**{role}:** {content}")
