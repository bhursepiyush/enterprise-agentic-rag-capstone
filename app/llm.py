import requests
from .config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

def generate(prompt: str) -> str:
    url = OLLAMA_BASE_URL.rstrip("/") + "/api/generate"
    r = requests.post(url, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=OLLAMA_TIMEOUT)
    r.raise_for_status()
    return r.json().get("response", "").strip()
