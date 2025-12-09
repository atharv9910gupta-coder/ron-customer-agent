Deployment Checklist (step-by-step)

Create a new repo named ron-customer-agent (or use your existing).

Create frontend/ and backend/ folders and copy files exactly.

On Supabase:

Create a project.

Run infra/supabase_schema.sql in the SQL editor.

Create an API key: SUPABASE_KEY (anon) and SUPABASE_SERVICE_KEY (service role). Keep service role secret for backend only.

Configure RLS policies as needed (or disable for testing).

Set environment secrets:

For Streamlit frontend (Streamlit Cloud): set GROQ_API_KEY, SUPABASE_URL, SUPABASE_KEY (anon for frontend).

For backend (Railway/Render): set SUPABASE_SERVICE_KEY, SMTP_*, TWILIO_*, BACKEND_SECRET.

Upload assets/logo.png via GitHub UI into frontend/assets/.

Deploy backend (Railway/Render); deploy frontend via Streamlit Cloud (connect frontend/).

Test Chat Support (create ticket, add message). Test email by calling backend /send-email with correct secret.
