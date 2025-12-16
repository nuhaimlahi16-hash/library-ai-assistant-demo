import json
import numpy as np
import faiss
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent  
DATA_PATH = BASE_DIR / "data" / "faq.json"
EMB_DIR = BASE_DIR / "embeddings"

INDEX_PATH = EMB_DIR / "faiss.index"
META_PATH  = EMB_DIR / "metadata.json"

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyCEyQ_ipICM-azlPlj-AvI5COQ9RRpBbXU"))

# Gemini embedding model
EMBED_MODEL = "models/embedding-001"


def chunk_text(text: str, max_length: int = 300):
    """Split text into smaller chunks for better embeddings."""
    words = text.split()
    chunks, current = [], []

    for w in words:
        current.append(w)
        if len(" ".join(current)) >= max_length:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def build_index():
    """Generate embeddings with Gemini + create FAISS index"""
    
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"faq.json missing at: {DATA_PATH}")

    with DATA_PATH.open("r", encoding="utf-8") as f:
        raw_faq = json.load(f)

    documents = []
    chunk_id = 0

    for item in raw_faq:
        question = item["question"]
        answer = item["answer"]

        for chunk in chunk_text(answer):
            documents.append({
                "chunk_id": chunk_id,
                "topic": question,
                "content": chunk
            })
            chunk_id += 1

    print("Generating embeddings using Gemini (free)...")

    vectors = []
    for doc in documents:
        emb = genai.embed_content(
            model=EMBED_MODEL,
            content=doc["content"],
            task_type="retrieval_document"
        )
        vectors.append(emb["embedding"])

    vectors = np.array(vectors, dtype="float32")

    # Create FAISS index
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    EMB_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    with META_PATH.open("w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)

    print(f"FAISS index built successfully! {len(documents)} chunks embedded.")


if __name__ == "__main__":
    build_index()
