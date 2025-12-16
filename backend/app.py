from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.faq_search import search_faq
from utils.search import search_faiss
from utils.llm import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask(data: Question):
    q = data.question

    faq = search_faq(q)
    if faq:
        return {
            "answer": (
                "Here is the information you requested:\n\n"
                f"- {faq}\n\n"
                "If you require further assistance, please contact the library staff."
            )
        }

    docs = search_faiss(q)
    answer = generate_answer(docs, q)

    return {"answer": answer}

@app.get("/")
def health():
    return {"status": "running"}
