# Capstone Documentation

## Objective
Build a Generative AI-powered enterprise document knowledge and decision-support system using LLMs, RAG, vector search, and autonomous agent stages.

## Agent roles
- Planner: normalizes the user question and determines that enterprise retrieval is required.
- Retriever: executes semantic search against ChromaDB.
- Reasoner: uses retrieved evidence and the Ollama LLM to draft a grounded answer.
- Validator: checks the draft against the same evidence and produces the final response.

## Data flow
1. User uploads PDF/TXT/CSV/XLSX.
2. Parser extracts text/tabular content.
3. Text is normalized and chunked.
4. Sentence Transformer creates embeddings.
5. ChromaDB stores embeddings, text and source metadata.
6. Query is embedded and top-k chunks are retrieved.
7. Reasoner receives question + evidence.
8. Validator reviews the answer against evidence.
9. UI displays answer, plan and retrieved sources.

## Deployment
Local deployment is the supported baseline. The API can later be containerized and deployed to a cloud VM/container platform. Secrets belong in environment variables, never in source control.

## Challenges
- Local model latency and memory usage.
- Retrieval quality depends on chunking and embedding model.
- PDF extraction may fail for scanned documents.
- LLM validation reduces unsupported responses but cannot provide mathematical certainty.
