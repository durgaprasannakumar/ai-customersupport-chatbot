1. Objective: Transform customer insights and market gaps (from VOC and research) into actionable product ideas. Use quantitative prioritization to identify which features enter the MVP versus later versions

2. Ideation Sources
Feature ideas were synthesized from:
    Voice of Customer (VOC) → unmet needs around speed, accuracy, transparency
    Market Research → gaps in explainability and multi-brand support
    Benchmarking → missing features in existing products like Zendesk AI, Intercom Fin
    Internal Goals → maintain transparency, minimize hallucination, ensure scalability

3. Brainstormed Feature Pool
| #  | Feature Idea                    | Description                                                            |
| -- | ------------------------------- | ---------------------------------------------------------------------- |
| 1  | **RAG Pipeline with Citations** | Core architecture: retrieve verified brand data, answer with citations |
| 2  | **Feedback Logging Mechanism**  | Capture user “helpful/unhelpful” votes for retraining                  |
| 3  | **Latency Optimization Layer**  | Pre-embed frequent queries, async model streaming                      |
| 4  | **Brand Filter Mode**           | Restrict answers to brand-specific content                             |
| 5  | **Confidence-based Fallbacks**  | If retrieval confidence < threshold → ask clarifying question          |
| 6  | **Dashboard for Analytics**     | Aggregate feedback, latency, and accuracy metrics                      |
| 7  | **Multi-turn Chat Memory**      | Maintain short context for 2–3 turns                                   |
| 8  | **Tone Control Prompting**      | Align responses with each brand’s voice (“friendly”, “formal”)         |
| 9  | **Offline Mode**                | Lightweight on-device model for internal demos                         |
| 10 | **Auto Retraining Loop**        | Periodic re-index using feedback and new data                          |

4. MoSCoW Prioritization
| Feature                  | Must | Should | Could | Won’t (Now) | Reason                   |
| ------------------------ | ---- | ------ | ----- | ----------- | ------------------------ |
| RAG pipeline + citations | ✅    |        |       |             | Core value proposition   |
| Feedback logging         | ✅    |        |       |             | Enables improvement loop |
| Brand filter             | ✅    |        |       |             | Multi-brand use cases    |
| Confidence fallback      |      | ✅      |       |             | Adds reliability         |
| Dashboard                |      | ✅      |       |             | PM insight & visibility  |
| Tone control             |      | ✅      |       |             | Brand alignment          |
| Multi-turn chat          |      |        | ✅     |             | Advanced UX              |
| Auto retraining          |      |        | ✅     |             | Long-term learning       |
| Offline mode             |      |        |       | ❌           | Not in MVP scope         |

5. RICE Scoring Matrix
| Feature             | Reach | Impact | Confidence | Effort | **RICE Score** |
| ------------------- | ----- | ------ | ---------- | ------ | -------------- |
| RAG pipeline        | 100   | 3      | 0.9        | 2      | 135            |
| Feedback logging    | 80    | 2      | 0.8        | 1      | 128            |
| Brand filter        | 70    | 2      | 0.9        | 1      | 126            |
| Confidence fallback | 60    | 2      | 0.7        | 2      | 84             |
| Dashboard           | 50    | 2      | 0.8        | 3      | 53             |
| Tone control        | 40    | 1      | 0.7        | 2      | 28             |

Interpretation:Top three features are RAG core, Feedback logging, and Brand filter , these define the MVP.

6. Idea Shortlisting (Based on PMT Lens)
| Lens           | Insight                          | Feature                |
| -------------- | -------------------------------- | ---------------------- |
| **Product**    | Must differentiate through trust | RAG + Citations        |
| **Market**     | SMBs need measurable ROI         | Feedback Dashboard     |
| **Technology** | Balance cost vs. speed           | Latency optimization   |
| **User**       | Users want transparency          | Brand + Citation combo |

7. User Story Mapping
| Epic                      | User Story                                                              | Acceptance Criteria                           |
| ------------------------- | ----------------------------------------------------------------------- | --------------------------------------------- |
| **Information Retrieval** | “As a customer, I want accurate, grounded answers so I can trust them.” | Must include ≥1 citation per answer           |
| **Feedback Capture**      | “As a user, I want to rate answers so the system improves over time.”   | Feedback stored & visible in logs             |
| **Brand Mode**            | “As an agent, I want responses filtered by my brand’s policies.”        | Only use documents tagged with selected brand |
| **Monitoring**            | “As a PM, I want to track performance metrics in a dashboard.”          | Accuracy, latency, and helpfulness displayed  |

8. Feature Dependency Graph
Core Dependencies:
    RAG → (Feedback, Brand Filter)
    Feedback → Dashboard
    Brand Filter → Tone Control
    Tone Control → Multi-turn Memory
Visual Flow:
    Data Layer (Kaggle dataset)
    ↓
    Retrieval Layer (FAISS)
    ↓
    Generation Layer (GPT/Claude)
    ↓
    UI Layer (Streamlit)
    ↓
    Feedback & Dashboard Layer

9. MVP Boundary
In Scope (V1)
    ✅ RAG with citations
    ✅ Feedback logging
    ✅ Brand filter
    ✅ Latency optimization

Out of Scope (Future)
    ❌ Multi-turn chat
    ❌ Voice or multilingual mode
    ❌ Offline LLM

10. Design Principle: “Every answer must be factual, fast, and explainable — or it should gracefully refuse.”