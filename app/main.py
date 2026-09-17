from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from .config import UPLOAD_DIR
from .ingestion import SUPPORTED, process_file
from .vector_store import VectorStore
from .agents import run_agent

app = FastAPI(title="Enterprise Agentic RAG API", version="1.0.0")
store = VectorStore()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok", "service": "Enterprise Agentic RAG"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED:
        raise HTTPException(400, f"Supported formats: {sorted(SUPPORTED)}")
    target = UPLOAD_DIR / Path(file.filename).name
    target.write_bytes(await file.read())
    chunks = process_file(target)
    count = store.add_chunks(chunks)
    return {"file": target.name, "chunks_indexed": count}

@app.post("/query")
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    return run_agent(req.question, store)
