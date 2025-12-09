# frontend/modules/memory.py
import streamlit as st

def get_history():
    if "history" not in st.session_state:
        st.session_state.history = []
    return st.session_state.history

def append_user(msg: str):
    hist = get_history()
    hist.append({"role":"user", "content": msg})
    st.session_state.history = hist

def append_assistant(msg: str):
    hist = get_history()
    hist.append({"role":"assistant", "content": msg})
    st.session_state.history = hist

def clear_history():
    st.session_state.history = []
