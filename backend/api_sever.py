# backend/api_server.py
import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from supabase import create_client
import smtplib
from email.message import EmailMessage
import requests

app = FastAPI()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # service role
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BACKEND_SECRET = os.getenv("BACKEND_SECRET")

class EmailPayload(BaseModel):
    to: str
    subject: str
    body: str
    secret: str

@app.post("/send-email")
async def send_email(payload: EmailPayload):
    if payload.secret != BACKEND_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")
    # Use SMTP settings from env
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = payload.to
    msg["Subject"] = payload.subject
    msg.set_content(payload.body)
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "sent"}

