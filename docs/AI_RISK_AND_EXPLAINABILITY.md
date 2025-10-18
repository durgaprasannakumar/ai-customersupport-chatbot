Risks
    Hallucination / Non‑compliance — mitigated by mandatory citations and refusal when no source.
    Bias/Toxic outputs — add safety instruction, simple toxicity filter on inputs/outputs.
    Privacy — no PII; run locally; redact handles if needed.
    Security — rate‑limit API keys; never log secrets.
    Model Drift — periodic re‑index and spot checks; log failure cases.

Explainability
    Show top‑k sources with confidence scores.
    Keep a deterministic prompt template and log it with each answer.
    Provide a “Why this answer” expander that lists retrieved snippets.

Evaluation Plan
    Weekly manual audit: 100 Q/A pairs, label as correct/incorrect/unsupported.
    Track hallucination rate, citation coverage, and time‑to‑answer.