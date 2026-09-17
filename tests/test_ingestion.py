from pathlib import Path
from app.ingestion import chunk_text, process_file

def test_chunk_overlap():
    chunks = chunk_text("a" * 2000, size=500, overlap=100)
    assert len(chunks) > 1
    assert all(len(c) <= 500 for c in chunks)

def test_txt_processing(tmp_path: Path):
    p = tmp_path / "demo.txt"
    p.write_text("Enterprise AI strategy and governance.", encoding="utf-8")
    rows = process_file(p)
    assert rows and rows[0]["source"] == "demo.txt"
