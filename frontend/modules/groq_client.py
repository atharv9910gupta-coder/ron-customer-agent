# frontend/modules/groq_client.py
import os, requests, json
from typing import List, Dict

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

def run_groq_chat(messages: List[Dict[str,str]], max_tokens: int=400, temperature: float=0.2) -> Dict:
    if not GROQ_API_KEY:
        return {"error": "GROQ API key not configured."}
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    try:
        r = requests.post(GROQ_URL, headers=headers, json=body, timeout=30)
    except Exception as e:
        return {"error": f"Network error: {e}"}
    try:
        data = r.json()
    except Exception:
        return {"error": f"Invalid JSON response ({r.status_code})."}
    if "error" in data:
        return {"error": data["error"]}
    # parse common shape
    try:
        return {"text": data["choices"][0]["message"]["content"], "raw": data}
    except Exception:
        return {"error": "Unexpected response shape from Groq."}

