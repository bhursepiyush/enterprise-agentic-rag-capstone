from pathlib import Path
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from .config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION, EMBEDDING_MODEL, TOP_K

class VectorStore:
    def __init__(self):
        Path(CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(CHROMA_COLLECTION)
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

    def add_chunks(self, chunks: List[Dict]):
        if not chunks:
            return 0
        ids = [f"{c['source']}::{c['chunk_id']}" for c in chunks]
        texts = [c["text"] for c in chunks]
        metas = [{"source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks]
        embeddings = self.embedder.encode(texts, normalize_embeddings=True).tolist()
        self.collection.upsert(ids=ids, documents=texts, metadatas=metas, embeddings=embeddings)
        return len(chunks)

    def search(self, query: str, k: int = TOP_K) -> List[Dict]:
        emb = self.embedder.encode([query], normalize_embeddings=True).tolist()
        result = self.collection.query(query_embeddings=emb, n_results=k)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [{"text": d, "source": m.get("source", "unknown"), "chunk_id": m.get("chunk_id"), "distance": dist}
                for d, m, dist in zip(docs, metas, distances)]
