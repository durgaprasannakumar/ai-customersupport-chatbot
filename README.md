# AI Customer Support Assistant (RAG + LLM)

---

## Project Overview

**Goal:** Build an explainable, retrieval-augmented customer support chatbot using LLMs (GPT-4 or Claude) grounded in real-world data from the Kaggle dataset [Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter).

**Problem:** Traditional AI chatbots hallucinate and fail to cite sources. Support teams need factual, policy-aligned responses that customers can trust.

**Solution:** A RAG-based (Retrieval-Augmented Generation) assistant that retrieves verified brand data, generates concise answers, and provides transparent citations — all accessible via a clean Streamlit UI.

---

## Features

* **Retrieval-Augmented Generation:** Combines FAISS vector search with GPT-4/Claude for factual responses.
* **Citations Panel:** Each answer includes references to original support tweets or FAQs.
* **Feedback Logging:** Users can mark answers as helpful/unhelpful, feeding continuous improvement.
* **Brand Filter:** Restrict results to a specific brand (AmazonHelp, Delta, AppleSupport, etc.).
* **Latency & Accuracy Metrics:** Real-time monitoring for grounded accuracy and performance.

---

## Architecture Overview

```
Data Layer (Kaggle Support Tweets)
   ↓
Embedding Layer (SentenceTransformer MiniLM)
   ↓
Retriever (FAISS Vector Index)
   ↓
Generator (GPT-4 / Claude API)
   ↓
Streamlit UI + Feedback Logger
```

---

## Dataset

**Source:** Kaggle – Customer Support on Twitter
**Rows:** 2.9M tweets
**Fields Used:** `author_id`, `inbound`, `created_at`, `text`
**Filtered:** inbound = True (customer queries only)

**Brands Represented:** AmazonHelp, Delta, AppleSupport, SpotifyCares, NikeSupport, Uber_Support

---

## Core Files

```
├── app/streamlit_app.py                 # Chat UI and feedback
├── pipeline/build_index.py              # FAISS index builder
├── notebooks/data_cleaning.ipynb        # Kaggle preprocessing
├── notebooks/evaluation_metrics.ipynb   # Accuracy/latency scoring
├── docs/PRD.md                          # Product Requirements
├── product_strategy_docs/               # Research, VOC, Ideation, MVP Plan
```

---

## Showcase

### **Chat Interface**

> AI Customer Support Assistant responding to “My Amazon package hasn’t arrived” — cites verified AmazonHelp sources for factual grounding.

### **Retrieval Visualization**

> Top-k retrieved snippets (FAISS cosine similarity) ranked by confidence, displaying brand context.

### **Feedback Dashboard**

> Real-time metrics — accuracy 91%, helpful votes 78%, latency under 3.5s P95.

### **Latency Distribution**

> Histogram of retrieval and generation times. 95th percentile latency = 3.4 seconds.

---

## Performance Metrics

| Metric            | Result | Target |
| ----------------- | ------ | ------ |
| Grounded Accuracy | 91%    | ≥90%   |
| Latency (P95)     | 3.4s   | ≤3.5s  |
| Helpful Feedback  | 78%    | ≥70%   |
| Citation Coverage | 100%   | 100%   |
| Deflection Rate   | 21%    | ≥20%   |

---

## Charts

| Chart                      | Insight                                      |
| -------------------------- | -------------------------------------------- |
| **Brand Distribution**     | AmazonHelp & Delta dominate inbound queries  |
| **Sentiment Distribution** | 62% negative → high automation potential     |
| **Accuracy vs Top-k**      | Accuracy plateaus at k=4 (optimal trade-off) |
| **Token vs Latency**       | Near-linear growth (~5ms/token)              |

---

## Evaluation Reports

| File                           | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| `grounded_accuracy_report.csv` | Grounded/hallucinated breakdown for 100 test queries |
| `user_feedback_log.csv`        | Session logs with helpfulness scores                 |
| `latency_summary.json`         | Aggregated latency metrics                           |

---

## MVP Highlights

| Component          | Delivered | Description                      |
| ------------------ | --------- | -------------------------------- |
| Retrieval Pipeline | ✅         | FAISS + embeddings (MiniLM)      |
| LLM Integration    | ✅         | GPT-4o and Claude APIs           |
| Feedback Loop      | ✅         | CSV-based logging and analytics  |
| Dashboard          | ✅         | Real-time Streamlit metrics view |
| Evaluation         | ✅         | Accuracy and latency reports     |

---

## Product Strategy Documents

All discovery-to-delivery materials are located in `/product_strategy_docs/`, including:

1. **01_background_survey** – Industry evolution & AI adoption trends
2. **02_market_research_document** – Competitive landscape & TAM analysis
3. **03_voice_of_customer_summary** – User pain points & sentiment insights
4. **04_ideation_and_feature_prioritization** – MoSCoW & RICE scoring
5. **05_mvp_and_implementation_plan** – Execution roadmap & KPIs

---


---

## Next Steps

* Add multi-turn chat memory (V2)
* Integrate live Zendesk API for ticket context
* Launch interactive Tableau dashboard for CX metrics
* Evaluate multilingual support for non-English tweets

---

## Key Takeaway

> This project demonstrates end-to-end **AI Product Management thinking** — from user pain discovery to technical delivery — showcasing skills across research, prioritization, prototyping, and product storytelling.

**Tags:** AI Product Management, RAG, Generative AI, Explainability, GPT-4, Claude, Kaggle, Streamlit, Product Analytics
