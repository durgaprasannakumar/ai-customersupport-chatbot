from dataclasses import dataclass


@dataclass
class Settings:
model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
top_k: int = 4
max_chunk_tokens: int = 220
overlap_tokens: int = 40