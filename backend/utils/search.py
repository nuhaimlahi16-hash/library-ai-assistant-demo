# utils/search.py
import json
import os
from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# -----------------------------
# ENV + GEMINI CONFIG
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = "models/embedding-001"

# -----------------------------
# FAISS RETRIEVER
# -----------------------------
class Retriever:
    def __init__(
        self,
        index_path: str = "embeddings/faiss.index",
        meta_path: str = "embeddings/metadata.json",
    ):
        self.index_path = Path(index_path)
        self.meta_path = Path(meta_path)

        if not self.index_path.exists() or not self.meta_path.exists():
            raise FileNotFoundError("FAISS index or metadata not found.")

        self.index = faiss.read_index(str(self.index_path))

        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.metadata: List[Dict] = json.load(f)

    def embed(self, text: str) -> List[float]:
        response = genai.embed_content(
            model=EMBED_MODEL,
            content=text,
            task_type="retrieval_query",
        )
        return response["embedding"]

    def search(self, query: str, top_k: int = 4) -> List[Dict]:
        vector = np.array([self.embed(query)], dtype="float32")
        _, indices = self.index.search(vector, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results


# -----------------------------
# FASTAPI ENTRY POINT
# -----------------------------
_retriever = None

def search_faiss(query: str, top_k: int = 4) -> List[Dict]:
    global _retriever

    if _retriever is None:
        _retriever = Retriever()

    return _retriever.search(query, top_k)
