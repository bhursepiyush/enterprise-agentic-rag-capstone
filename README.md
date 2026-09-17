# Enterprise Agentic RAG Capstone

A learning-oriented implementation of the attached capstone brief: multi-format document ingestion, chunking, embeddings, Chroma vector search, RAG, and an agent workflow with Planner → Retriever → Reasoner → Validator.

## Requirements
- Windows 10/11, macOS, or Linux
- Python 3.11 recommended
- Git
- Ollama
- 8 GB+ RAM recommended

## 1. Install software
Install Python from https://www.python.org/downloads/ and Git from https://git-scm.com/downloads/. Install Ollama from https://ollama.com/.

Verify:
```bash
python --version
git --version
ollama --version
```

Pull a small local model:
```bash
ollama pull llama3:latest
```

## 2. Create environment
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

## 3. Run tests
```bash
pytest -q
```

## 4. Start API
```bash
uvicorn app.main:app --reload --port 8000
```
Open http://127.0.0.1:8000/docs

## 5. Start UI (second terminal)
Activate the same venv, then:
```bash
streamlit run app/streamlit_app.py
```
Open the URL shown by Streamlit, usually http://localhost:8501.

## 6. Test end-to-end
Upload the sample files from `data/sample_docs/`. Ask:
- What are the strategic pillars of Orion's AI strategy?
- What controls are required for high-impact AI workflows?
- What are the monthly cloud costs and which team owns LLM inference?
- What should the assistant do when supporting evidence is unavailable?

The answer should be grounded in retrieved chunks and show the agent plan/evidence.

## Architecture
User → Streamlit → FastAPI → Planner → Chroma semantic retrieval → Reasoner/LLM → Validator → grounded answer + evidence.

## Project-to-brief mapping
1. Foundation: repository, config, API/UI.
2. Interaction: Streamlit upload + question UI and FastAPI.
3. Ingestion: PDF/TXT/CSV/Excel.
4. Chunking: configurable chunk size/overlap.
5. Vector store: Sentence Transformers + ChromaDB.
6. Retrieval: semantic similarity search.
7. RAG: context + local Ollama LLM.
8. Agents: Planner, Retriever, Reasoner, Validator workflow.
9. Reliability: input validation, supported formats, grounded prompts, validation step.
10. Documentation/deployment: this README plus local execution steps.

## Limitations
- Local LLM quality depends on the Ollama model and hardware.
- Scanned/image-only PDFs need OCR, which is not included in this starter.
- Authentication, production observability, distributed vector DB, and cloud deployment are intentionally outside the minimal local capstone implementation.
- The validator is another LLM pass; it is not a formal guarantee against hallucinations.
