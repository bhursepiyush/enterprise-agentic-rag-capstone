from pathlib import Path
from typing import List, Dict
import io
import pandas as pd
from pypdf import PdfReader
from .config import CHUNK_SIZE, CHUNK_OVERLAP

SUPPORTED = {".pdf", ".txt", ".csv", ".xlsx", ".xls"}

def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if ext in {".csv", ".xlsx", ".xls"}:
        if ext == ".csv":
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        return df.to_csv(index=False)
    raise ValueError(f"Unsupported file type: {ext}")

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    text = " ".join(text.split())
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def process_file(path: Path) -> List[Dict]:
    text = extract_text(path)
    return [{"text": c, "source": path.name, "chunk_id": i} for i, c in enumerate(chunk_text(text))]
