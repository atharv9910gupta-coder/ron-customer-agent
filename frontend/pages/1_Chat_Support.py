# frontend/pages/1_Chat_Support.py
import streamlit as st
from modules import groq_client, memory, db

st.header("💬 Chat Support — Agent")

# Choose ticket to attach message to (or create new)
tickets = db.list_tickets(100)
ticket_options = ["Create new ticket"] + [f"{t['id']} — {t['title']}" for t in tickets]
choice = st.selectbox("Ticket", ticket_options)

if choice == "Create new ticket":
    new_title = st.text_input("Ticket title")
    new_desc = st.text_area("Description")
    if st.button("Create ticket"):
        created = db.create_ticket(new_title, new_desc)
        st.success(f"Created ticket {created.get('id')}")
        st.experimental_rerun()
else:
    selected_id = int(choice.split(" — ")[0])
    st.subheader(f"Ticket {selected_id}")
    st.write("Conversation attached to ticket.")

    # show existing messages
    msgs = db.get_ticket_messages(selected_id)
    if msgs:
        for m in msgs:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "user":
                st.markdown(f"- **Customer:** {content}")
            else:
                st.markdown(f"- **Agent:** {content}")
    else:
        st.info("No messages yet for this ticket.")

    # input area
    user_msg = st.text_input("Your reply (will be sent by AI):", key=f"reply_{selected_id}")
    if st.button("Send AI reply"):
        if not user_msg.strip():
            st.warning("Type something first.")
        else:
            # build messages: system + history
            system = {"role":"system", "content": "You are RON, helpful customer support agent."}
            history = db.get_ticket_messages(selected_id)
            # convert history to groq messages format
            groq_history = [system] + [{"role": m["role"], "content": m["content"]} for m in history]
            groq_history.append({"role":"user","content": user_msg})
            out = groq_client.run_groq_chat(groq_history)
            if "error" in out:
                st.error(out["error"])
            else:
                reply = out.get("text","")
                # append both user and assistant messages to ticket
                db.append_ticket_message(selected_id, "user", user_msg)
                db.append_ticket_message(selected_id, "assistant", reply)
                st.success("AI replied and saved to ticket.")
                st.experimental_rerun()
