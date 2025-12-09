# frontend/modules/tools.py
import os
import requests

BACKEND_SEND_EMAIL = os.getenv("BACKEND_SEND_EMAIL_URL")  # optional server endpoint

def send_email_placeholder(to_email: str, subject: str, body: str) -> dict:
    if BACKEND_SEND_EMAIL:
        try:
            r = requests.post(BACKEND_SEND_EMAIL, json={"to": to_email, "subject": subject, "body": body}, timeout=20)
            return {"ok": r.status_code in (200,201), "response": r.text}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    return {"ok": False, "error": "Email sending not configured. Set BACKEND_SEND_EMAIL or implement SMTP."}
