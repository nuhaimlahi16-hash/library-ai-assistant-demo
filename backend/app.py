from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.faq_search import search_faq
from utils.search import search_faiss
from utils.llm import generate_answer

app = FastAPI(title="ALVIN – Library AI Assistant (Demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(data: Question):
    question = data.question

    # 1. FAQ first
    faq_answer = search_faq(question)
    if faq_answer:
        return {"answer": faq_answer}

    # 2. Semantic search + LLM
    context = search_faiss(question)
    answer = generate_answer(context, question)

    return {"answer": answer}

@app.get("/")
def health_check():
    return {"status": "ALVIN demo backend running"}
