from typing import Dict, List
from .llm import generate

SYSTEM_RULES = """You are an enterprise document QA assistant. Use ONLY the supplied context.
If the context does not contain the answer, say: 'I could not find enough information in the uploaded documents.'
Never invent facts, numbers, policies, or citations. Cite sources as [1], [2], etc."""

def planner(query: str) -> Dict:
    q = query.strip()
    return {"needs_retrieval": True, "planned_query": q, "reason": "Enterprise knowledge question; retrieve evidence before answering."}

def build_context(results: List[Dict]) -> str:
    return "\n\n".join(f"[{i}] Source: {r['source']}\n{r['text']}" for i, r in enumerate(results, 1))

def reason(query: str, results: List[Dict]) -> str:
    context = build_context(results)
    prompt = f"{SYSTEM_RULES}\n\nQuestion: {query}\n\nContext:\n{context}\n\nAnswer with a concise, evidence-grounded response."
    return generate(prompt)

def validate(query: str, answer: str, results: List[Dict]) -> str:
    context = build_context(results)
    prompt = f"""You are a validation agent. Check whether the answer is supported by the context.
Return ONLY the corrected final answer. If unsupported, say you could not find enough information.
Question: {query}\nAnswer: {answer}\nContext:\n{context}"""
    return generate(prompt)

def run_agent(query: str, store) -> Dict:
    plan = planner(query)
    results = store.search(plan["planned_query"])
    if not results:
        return {"answer": "I could not find enough information in the uploaded documents.", "plan": plan, "sources": []}
    draft = reason(query, results)
    final = validate(query, draft, results)
    return {"answer": final, "draft": draft, "plan": plan, "sources": results}
