# RON Backend

## Overview
FastAPI backend for RON customer-support app.
Provides secure endpoints for tickets, messages, email sending, and Twilio webhooks.

## Required environment variables (set on hosting provider)
- SUPABASE_URL
- SUPABASE_SERVICE_KEY   (service role key — server only)
- BACKEND_SECRET         (a long random string)
- SMTP_HOST
- SMTP_PORT
- SMTP_USER
- SMTP_PASS
- TWILIO_AUTH_TOKEN      (optional)
- FRONTEND_URL           (optional, used in email templates)

## Run locally
1. Create .env file:
