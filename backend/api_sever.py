# backend/api_server.py
import os
import smtplib
from email.message import EmailMessage
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # load from .env when testing locally

# ---------- ENV / CONFIG ----------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # <- must be service_role key on server
BACKEND_SECRET = os.getenv("BACKEND_SECRET", "change_this_long_secret")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")  # if needed for validation (optional)
FRONTEND_URL = os.getenv("FRONTEND_URL", "")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment for the backend to run.")

# supabase client (server)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = FastAPI(title="RON Backend API")


# ---------- Pydantic models ----------
class CreateTicketPayload(BaseModel):
    title: str
    description: Optional[str] = ""
    requester_email: Optional[EmailStr] = None
    secret: str


class AppendMessagePayload(BaseModel):
    ticket_id: int
    role: str  # 'user' | 'agent' | 'system'
    content: str
    secret: str


class SendEmailPayload(BaseModel):
    to: EmailStr
    subject: str
    body: str
    secret: str


# ---------- Helpers ----------
def verify_secret(secret: str):
    if secret != BACKEND_SECRET:
        raise HTTPException(status_code=403, detail="Invalid backend secret")


def send_email_smtp(to_email: str, subject: str, body: str) -> Dict[str, Any]:
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS]):
        return {"ok": False, "error": "SMTP is not configured on server."}

    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------- Routes ----------
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/tickets/create")
async def create_ticket(payload: CreateTicketPayload):
    verify_secret(payload.secret)
    row = {
        "title": payload.title,
        "description": payload.description,
        "requester_email": payload.requester_email,
        "status": "open"
    }
    try:
        res = supabase.table("tickets").insert(row).execute()
        if hasattr(res, "status_code") and res.status_code in (200, 201):
            return {"ok": True, "ticket": res.data[0]}
        # older client structure
        return {"ok": True, "ticket": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tickets/list")
async def list_tickets(limit: int = 100, secret: str = ""):
    verify_secret(secret)
    try:
        res = supabase.table("tickets").select("*").order("created_at", desc=True).limit(limit).execute()
        return {"ok": True, "tickets": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tickets/append")
async def append_message(payload: AppendMessagePayload):
    verify_secret(payload.secret)
    # store message in messages table and optionally return current messages
    row = {
        "ticket_id": payload.ticket_id,
        "role": payload.role,
        "content": payload.content
    }
    try:
        res = supabase.table("messages").insert(row).execute()
        # also optionally update ticket metadata
        return {"ok": True, "message": res.data[0] if hasattr(res, "data") else res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tickets/{ticket_id}/messages")
async def get_ticket_messages(ticket_id: int, secret: str = ""):
    verify_secret(secret)
    try:
        res = supabase.table("messages").select("*").eq("ticket_id", ticket_id).order("created_at", desc=False).execute()
        return {"ok": True, "messages": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-email")
async def send_email(payload: SendEmailPayload, background_tasks: BackgroundTasks):
    # validate secret
    verify_secret(payload.secret)
    # send in background to return fast
    background_tasks.add_task(send_email_smtp, payload.to, payload.subject, payload.body)
    return {"ok": True, "note": "Email scheduled (background)."}


# Twilio webhook for SMS or voice events (simple example)
@app.post("/twilio/webhook")
async def twilio_webhook(request: Request):
    # Optional: validate Twilio signature if you want (not included)
    form = await request.form()
    # Twilio sends fields like From, To, Body for SMS
    tw_from = form.get("From")
    tw_body = form.get("Body")
    # Save as a ticket or message based on your flow
    try:
        # create a ticket if needed
        title = f"SMS from {tw_from}"
        desc = tw_body or "(empty)"
        res = supabase.table("tickets").insert({"title": title, "description": desc, "requester_email": None}).execute()
        # insert initial message
        ticket = res.data[0]
        supabase.table("messages").insert({"ticket_id": ticket["id"], "role": "user", "content": tw_body}).execute()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
