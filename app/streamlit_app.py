import os, time, pickle
import streamlit as st
import numpy as np
import faiss
import pandas as pd
from pathlib import Path

#LLM backends
USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None
USE_ANTHROPIC = os.getenv("ANTHROPIC_API_KEY") is not None

if USE_OPENAI:
    from openai import OpenAI
    oai = OpenAI()
if USE_ANTHROPIC:
    import anthropic
    client = anthropic.Anthropic()

INDEX_PATH = "data/index.faiss"
STORE_PATH = "data/store.pkl"
DATA_PATH = "data/support_tweets_sample.csv"

st.set_page_config(page_title="AI Support Assistant", layout="wide")

st.sidebar.title("Settings")
brand_filter = st.sidebar.text_input("Brand filter (optional)")
top_k = st.sidebar.slider("Top‑K", 1, 8, 4)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2)

st.title("AI Customer Support Assistant — RAG")

@st.cache_resource(show_spinner=False)
def load_index():
    if not Path(INDEX_PATH).exists() or not Path(STORE_PATH).exists():
        st.error("Index not found. Please run the indexing step first.")
        st.stop()
    index = faiss.read_index(INDEX_PATH)
    with open(STORE_PATH, "rb") as f:
        store = pickle.load(f)
    meta = store["meta"]
    return index, meta

index, meta = load_index()

# Build quick dataframe for filtering
meta_df = pd.DataFrame(meta)

chat_history = st.session_state.setdefault("history", [])
user_q = st.chat_input("Ask a support question…")


def retrieve(question, top_k=4, brand=None):
    # Lazy embed via OpenAI text-embedding-3-small if available, else cosine with naive TF-IDF fallback
    import numpy as np
    try:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        q_vec = m.encode([question], normalize_embeddings=True)[0].astype("float32")
    except Exception as e:
        st.error(f"Embedding model failed: {e}")
        raise

    D, I = index.search(np.array([q_vec]), top_k*5)  # retrieve more, filter by brand later
    hits = []
    for score, idx in zip(D[0].tolist(), I[0].tolist()):
        if idx == -1: continue
        row = meta[idx]
        if brand and str(row.get("brand", "")).lower() != brand.lower():
            continue
        hits.append({"score": float(score), **row, "id": str(idx)})
        if len(hits) >= top_k:
            break
    return hits


def compose_prompt(question, passages):
    context = "\n\n".join([f"[[{i+1}]] {p['text']} (brand={p['brand']}, date={p['created_at']})" for i, p in enumerate(passages)])
    sys = (
        "You are a precise, policy‑following support assistant. "
        "Answer ONLY from the provided sources. If insufficient, say you don't know and ask for clarification. "
        "Always include citation markers like [1], [2] that map to the provided sources."
    )
    user = f"Question: {question}\n\nSources:\n{context}"
    return sys, user


def generate_answer(system_prompt, user_prompt, temperature=0.2):
    t0 = time.time()
    if USE_OPENAI:
        chat = oai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
            temperature=temperature,
        )
        ans = chat.choices[0].message.content
        gen_ms = (time.time()-t0)*1000
        tokens_in = chat.usage.prompt_tokens if hasattr(chat, "usage") else None
        tokens_out = chat.usage.completion_tokens if hasattr(chat, "usage") else None
        return ans, gen_ms, tokens_in, tokens_out
    elif USE_ANTHROPIC:
        msg = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=600,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role":"user","content":user_prompt}],
        )
        ans = msg.content[0].text
        gen_ms = (time.time()-t0)*1000
        return ans, gen_ms, None, None
    else:
        return "[LLM key missing] Please set OPENAI_API_KEY or ANTHROPIC_API_KEY.", 0, None, None


if user_q:
    st.chat_message("user").markdown(user_q)
    t0 = time.time()
    hits = retrieve(user_q, top_k=top_k, brand=brand_filter or None)
    ret_ms = (time.time()-t0)*1000

    if not hits:
        st.chat_message("assistant").warning("I couldn't find relevant sources. Try removing the brand filter or rephrasing.")
    else:
        sys_p, usr_p = compose_prompt(user_q, hits)
        ans, gen_ms, tin, tout = generate_answer(sys_p, usr_p, temperature)

        # Render answer
        with st.chat_message("assistant"):
            st.markdown(ans)
            with st.expander("Sources"):
                for i, h in enumerate(hits, 1):
                    st.write(f"[{i}] {h['text']}  ")
                    st.caption(f"brand={h['brand']} • date={h['created_at']} • score={h['score']:.3f}")
            st.caption(f"Retrieval: {ret_ms:.0f} ms • Generation: {gen_ms:.0f} ms • tokens_in={tin} • tokens_out={tout}")

        # Feedback row
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Helpful", use_container_width=True):
                pd.DataFrame([{"question": user_q, "answer": ans, "helpful": True}]).to_csv("data/feedback.csv", mode="a", index=False, header=not os.path.exists("data/feedback.csv"))
        with col2:
            if st.button("👎 Not helpful", use_container_width=True):
                pd.DataFrame([{"question": user_q, "answer": ans, "helpful": False}]).to_csv("data/feedback.csv", mode="a", index=False, header=not os.path.exists("data/feedback.csv"))
