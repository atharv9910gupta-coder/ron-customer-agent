# frontend/modules/db.py
import os
import json
from typing import List, Dict, Any

# If supabase is configured, use it. Otherwise use JSON file local storage.
USE_SUPABASE = bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"))

DATA_DIR = "data"
CHATS_FILE = os.path.join(DATA_DIR, "chats.json")
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, "w", encoding="utf8") as f:
            json.dump({}, f)
    if not os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "w", encoding="utf8") as f:
            json.dump([], f)

# Local JSON helpers
def load_chats_local() -> Dict[str, Any]:
    ensure_data_dir()
    try:
        with open(CHATS_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_chats_local(chats: Dict[str, Any]):
    ensure_data_dir()
    with open(CHATS_FILE, "w", encoding="utf8") as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)

def load_tickets_local() -> List[Dict[str,Any]]:
    ensure_data_dir()
    try:
        with open(TICKETS_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    except Exception:
        return []

def save_tickets_local(tickets):
    ensure_data_dir()
    with open(TICKETS_FILE, "w", encoding="utf8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

# Public API (fallback to local)
def list_tickets(limit:int=100) -> List[Dict[str,Any]]:
    if USE_SUPABASE:
        try:
            from supabase import create_client
            supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
            res = supabase.table("tickets").select("*").order("created_at", desc=True).limit(limit).execute()
            return res.data if getattr(res, "data", None) is not None else []
        except Exception:
            return load_tickets_local()
    else:
        return load_tickets_local()

def create_ticket(title: str, description: str, requester_email: str = None) -> Dict[str,Any]:
    if USE_SUPABASE:
        try:
            from supabase import create_client
            supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
            row = {"title": title, "description": description, "requester_email": requester_email}
            res = supabase.table("tickets").insert(row).execute()
            return res.data[0] if res.status_code in (200,201) else {"error": res}
        except Exception:
            pass
    # local fallback: append to list with id
    tickets = load_tickets_local()
    new_id = (tickets[-1].get("id", 0) + 1) if tickets else 1
    t = {"id": new_id, "title": title, "description": description, "requester_email": requester_email, "status": "open"}
    tickets.insert(0, t)
    save_tickets_local(tickets)
    return t

def get_ticket_messages(ticket_id: int) -> List[Dict[str,str]]:
    chats = load_chats_local()
    return chats.get(str(ticket_id), [])

def append_ticket_message(ticket_id: int, role: str, content: str):
    chats = load_chats_local()
    key = str(ticket_id)
    if key not in chats:
        chats[key] = []
    chats[key].append({"role": role, "content": content})
    save_chats_local(chats)
    return True
