Decision Memo — RAG baseline with GPT‑4 (vs. fine‑tuning)

Decision: Start with retrieval‑augmented generation using a strong general LLM (GPT‑4 or Claude) + all-MiniLM-L6-v2 retriever. Do not fine‑tune for MVP.

Why (PM trade‑offs):
Time‑to‑value: RAG delivers grounded answers immediately; fine‑tuning requires labeled pairs and evaluation infra.
Risk: Fine‑tuned models can still hallucinate without retrieval; governance prefers citations.
Cost: Inference‑only with caching; fine‑tune adds training cost + ongoing drift management.
Iterability: RAG lets us iterate on the data layer (docs, chunking, negatives) which is faster than model training cycles.

Alternatives considered:
Small local LLM (e.g., Llama‑3 8B) only: cheaper, but weaker reasoning and safety; still needs RAG.
Fine‑tune open‑source model: useful later for tone/style; not needed to achieve accuracy with citations.

Next check‑points:
If grounded accuracy <90% after prompt + retrieval tuning, explore lightweight adapter‑tuning for style and guardrails.