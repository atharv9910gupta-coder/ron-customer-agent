# backend/worker.py
import time
from datetime import datetime, timedelta
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("Supabase config missing for worker.")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def run_cleanup():
    # Example: close tickets older than 180 days (just illustrating)
    cutoff = (datetime.utcnow() - timedelta(days=180)).isoformat()
    q = supabase.table("tickets").update({"status":"closed"}).lt("created_at", cutoff).execute()
    print("Cleanup run:", q)

if __name__ == "__main__":
    while True:
        try:
            run_cleanup()
        except Exception as e:
            print("Worker error:", e)
        time.sleep(60 * 60 * 24)  # run once per day

