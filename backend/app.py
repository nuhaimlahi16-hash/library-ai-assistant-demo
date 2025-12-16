from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.faq_search import search_faq
from utils.search import search_faiss
from utils.llm import generate_answer
from utils.translator import translate_text

app = FastAPI(title="ALVIN – M6 Library Assistant")

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
# AI ENDPOINT
# -----------------------------
@app.post("/ask")
async def ask_question(data: Question):
    user_q = data.question.strip()

    # 1️⃣ FAQ FIRST (authoritative answers)
    faq_answer = search_faq(user_q)
    if faq_answer:
        formatted = f"""
        <p><strong>Here is the information you requested:</strong></p>
        <ul>
            {''.join(f'<li>{line.strip()}</li>' for line in faq_answer.split(';'))}
        </ul>
        <p>If you need further clarification, please contact the library staff at
        <a href="mailto:researchandlearning@aui.ma">researchandlearning@aui.ma</a>.</p>
        """
        return {"answer": formatted}

    # 2️⃣ FAISS + GEMINI
    docs = search_faiss(user_q)
    answer = generate_answer(docs, user_q)
    answer = translate_text(answer)

    # Enforce professional formatting
    formatted_answer = f"""
    <p><strong>Here is the information you requested:</strong></p>
    <p>{answer}</p>
    <p>If you need additional assistance, please contact the library staff at
    <a href="mailto:researchandlearning@aui.ma">researchandlearning@aui.ma</a>.</p>
    """

    return {"answer": formatted_answer}

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {"status": "ALVIN is running"}
