# frontend/modules/groq_client.py
import os
import requests
import json
from typing import List, Dict

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

def run_groq_chat(messages: List[Dict[str,str]], max_tokens: int = 300, temperature: float = 0.2) -> Dict:
    """
    messages: list of {"role": "...", "content": "..."}
    returns: dict with either {'text': "..."} or {'error': "..."}
    """
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY not configured. Add it to Streamlit Secrets or environment variables."}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    try:
        r = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    except Exception as e:
        return {"error": f"Network error calling Groq: {e}"}

    try:
        data = r.json()
    except Exception:
        return {"error": f"Invalid JSON from Groq (status {r.status_code})."}

    if isinstance(data, dict) and "error" in data:
        # return error message
        try:
            msg = data["error"].get("message", str(data["error"]))
        except Exception:
            msg = str(data["error"])
        return {"error": f"Groq API error: {msg}"}

    # Extract message text safely
    try:
        choices = data.get("choices")
        if choices and isinstance(choices, list):
            content = choices[0].get("message", {}).get("content", "")
            if content:
                return {"text": content}
    except Exception:
        pass

    # fallback: try other fields
    if "output" in data:
        return {"text": str(data["output"])}
    if "text" in data:
        return {"text": str(data["text"])}
    return {"error": "Unexpected Groq response shape."}
