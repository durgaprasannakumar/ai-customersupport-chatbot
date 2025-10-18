Product Requirements Document — AI Customer Support Assistant

1. Problem & Context
Customer support teams spend excessive time repeating answers across channels. Generic LLMs hallucinate or contradict policies. We need fast, accurate, cited answers grounded in our own knowledge.

2. Users & Jobs‑to‑Be‑Done
Agents: “Give me a policy‑correct response with links I can paste.”
End customers: “Answer my question instantly and correctly.”
Managers/PMs: “See top issues, quality trends, and deflection ROI.”

3. Goals & Non‑Goals
Goals:
    ≥90% grounded response accuracy (manual spot checks)
    20% ticket deflection (simulated via FAQ click‑throughs)
    <1.5s P95 retrieval latency; <3.5s P95 end‑to‑end
    100% of answers include citations
Non‑Goals (MVP): 
    multi‑turn tool use (refund APIs), escalation routing, PII ingestion.

4. KPIs
Quality: grounded‑accuracy %, citation coverage, hallucination rate
Efficiency: latency (retrieval + generation), tokens per answer
Business: deflection rate, AHT reduction (simulated), CSAT proxy (thumbs up/down)

5. Data Sources
Uses Kaggle's Customer Support on Twitter dataset (3M+ rows) as the knowledge base. Only inbound customer queries are indexed; optional brand filter allows contextual retrieval.

6. Solution Overview
Embed documents with all-MiniLM-L6-v2
Store vectors in FAISS + Python pickle store for metadata
Retrieve top‑k passages → prompt LLM with system instruction + citations
Streamlit UI with chat, sources, and feedback buttons

7. Requirements
Functional
    Upload/ingest CSV or folder of .md/.txt
    Build/refresh index
    Ask question → show answer + k sources with brand, date, excerpt
    Thumbs up/down logging to data/feedback.csv

Non‑Functional
    Local run on CPU
    Secrets via environment variables
    Clear errors when no source found

8. UX
Left panel: brand filter, top‑k slider (1–8), temperature slider
Main: chat transcript; each answer shows citations; copy button
Footer: latency + tokens; feedback widget

9. Risks & Mitigations (see also Risk memo)
Dataset includes real tweets — ensure no PII exposure and comply with Twitter TOS by using derived text only.
Hallucination → enforce citation requirement; answer must quote [[n]] markers
Bias/toxicity → safety system prompt; blocklist in pre‑processor
Data leakage → local, no PII, rate‑limited keys

10. Rollout & Roadmap
MVP (this repo): RAG + citations + feedback logging
V1: Evaluation harness, auto‑refresh pipeline, basic analytics tab
V2: Tool use (order status API), role prompts, multi‑brand tenants