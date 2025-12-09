
# frontend/modules/db.py
import os
from supabase import create_client, Client
from typing import Any, Dict, List

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_tickets(limit: int=100) -> List[Dict[str, Any]]:
    res = supabase.table("tickets").select("*").order("created_at", desc=True).limit(limit).execute()
    return res.data if res.status_code == 200 else []

def create_ticket(title: str, description: str, requester_email: str = None) -> Dict:
    payload = {"title": title, "description": description, "requester_email": requester_email}
    res = supabase.table("tickets").insert(payload).execute()
    return res.data[0] if res.status_code == 201 else {"error": res}

def append_message(ticket_id: int, role: str, content: str):
    payload = {"ticket_id": ticket_id, "role": role, "content": content}
    res = supabase.table("messages").insert(payload).execute()
    return res.data if res.status_code == 201 else {"error": res}
