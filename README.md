# Project Overview

Goal: Build an AI-powered RAG chatbot that can answer customer support questions using real Twitter data from major brands.

Dataset Used: Customer Support on Twitter - Kaggle
Data Columns: tweed_id, author_id, inbound, created_at, text, response_tweet_id, in_response_to_tweet_id

Cleaned Schema for Indexing: brand,	created_at, text

Pipeline Summary:
    Clean raw data (retain inbound customer queries)
    Build FAISS vector index (SentenceTransformers)
    Retrieve relevant passages (brand-specific)
    Generate grounded answers (OpenAI GPT‑4 / Anthropic Claude)
    Streamlit UI for chat + feedback

Quickstart

Create a virtual environment and install deps:
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
Add keys in .env (see .env.example).
Put a CSV at data/support_tweets_sample.csv with columns: brand, created_at, text (see schema below).
Build the index:
    python -m pipeline.build_index --input data/support_tweets_sample.csv --index_path data/index.faiss --store_path data/store.pkl
Run the app:
    streamlit run app/streamlit_app.py