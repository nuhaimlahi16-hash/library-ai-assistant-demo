from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.faq_search import search_faq
from utils.search import search_faiss
from utils.llm import generate_answer

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REQUEST MODEL
# -----------------------------
class Question(BaseModel):
    question: str

# -----------------------------
# ASK ENDPOINT
# -----------------------------
@app.post("/ask")
async def ask_question(data: Question):
    question = data.question.strip()

    # 1) FAQ FIRST
    faq_answer = search_faq(question)
    if faq_answer:
        return {
            "answer": format_answer(faq_answer)
        }

    # 2) FAISS + LLM
    docs = search_faiss(question)
    ai_answer = generate_answer(docs, question)

    return {
        "answer": ai_answer
    }

# -----------------------------
# FORMAT FAQ ANSWERS
# -----------------------------
def format_answer(text: str) -> str:
    """
    Convert plain FAQ answers into
    formal bullet-point responses.
    """
    lines = text.split(";")
    bullets = "\n".join([f"- {line.strip()}" for line in lines])

    return (
        "Here is the information you requested:\n\n"
        f"{bullets}\n\n"
        "If you require further clarification, "
        "please contact the library staff."
    )

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {"status": "ALVIN backend is running"}
