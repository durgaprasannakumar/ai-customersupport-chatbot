import argparse, os, pickle, time
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from pathlib import Path

from config import Settings

S = Settings()


def chunk_text(text, max_tokens=220, overlap=40):
    # naive chunker by words (proxy for tokens)
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+max_tokens]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        i += max_tokens - overlap
    return chunks or [text]


def main(input_csv, index_path, store_path):
    t0 = time.time()
    df = pd.read_csv(input_csv)
    assert set(["brand", "created_at", "text"]).issubset(df.columns), "CSV missing required columns"

    # Build corpus of passages
    records = []
    for _, row in df.iterrows():
        for ch in chunk_text(str(row["text"]), S.max_chunk_tokens, S.overlap_tokens):
            records.append({
                "brand": row["brand"],
                "created_at": row["created_at"],
                "text": ch
            })
    corpus = pd.DataFrame(records)

    # Embeddings
    model = SentenceTransformer(S.model_name)
    vectors = model.encode(corpus["text"].tolist(), batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    vectors = np.array(vectors).astype("float32")

    # FAISS index (IP for cosine since normalized)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    # Save
    faiss.write_index(index, index_path)
    with open(store_path, "wb") as f:
        pickle.dump({"meta": corpus.to_dict(orient="records")}, f)

    print(f"Built index with {len(corpus)} passages in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--index_path", required=True)
    ap.add_argument("--store_path", required=True)
    args = ap.parse_args()

    Path(os.path.dirname(args.index_path)).mkdir(parents=True, exist_ok=True)
    Path(os.path.dirname(args.store_path)).mkdir(parents=True, exist_ok=True)

    main(args.input, args.index_path, args.store_path)