import requests
import streamlit as st

st.set_page_config(page_title="Enterprise Agentic RAG", layout="wide")
st.title("Enterprise Document QA — Agentic RAG")
st.caption("Planner → Retriever → Reasoner → Validator")
API = st.sidebar.text_input("API URL", "http://127.0.0.1:8000")

uploaded = st.file_uploader("Upload PDF, TXT, CSV or Excel", type=["pdf","txt","csv","xlsx","xls"])
if uploaded and st.button("Ingest document"):
    with st.spinner("Uploading and indexing..."):
        r = requests.post(f"{API}/upload", files={"file": (uploaded.name, uploaded.getvalue())}, timeout=180)
    if r.ok: st.success(r.json())
    else: st.error(r.text)

q = st.text_input("Ask a question about your uploaded documents")
if st.button("Ask") and q:
    with st.spinner("Agent workflow running..."):
        r = requests.post(f"{API}/query", json={"question": q}, timeout=240)
    if r.ok:
        data = r.json()
        st.subheader("Answer")
        st.write(data["answer"])
        with st.expander("Agent plan"):
            st.json(data["plan"])
        with st.expander("Retrieved evidence"):
            for i, s in enumerate(data["sources"], 1):
                st.markdown(f"**[{i}] {s['source']} — chunk {s['chunk_id']}**")
                st.write(s["text"])
    else: st.error(r.text)
