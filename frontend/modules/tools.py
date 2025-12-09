# frontend/modules/tools.py
import os, requests
def send_email_smtp(to, subject, body):
    # For security, call backend API to send email using service role key
    raise NotImplementedError("Use backend endpoint to send email securely.")
def send_sms_twilio(to, message):
    raise NotImplementedError("Use backend endpoint to send SMS securely.")

