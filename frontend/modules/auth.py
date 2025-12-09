# frontend/modules/auth.py
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_in(email: str, password: str):
    return supabase.auth.sign_in(email=email, password=password)

def sign_up(email: str, password: str):
    return supabase.auth.sign_up({"email": email, "password": password})

def get_user():
    return supabase.auth.user()

