import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash"

SYSTEM_PROMPT = """
You are ALVIN, a university library assistant demo.
Your role is to provide general, formal, and helpful answers.

Rules:
- Use bullet points when appropriate
- Keep responses professional
- If unsure, suggest contacting library staff
"""

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    response = genai.GenerativeModel(MODEL).generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )

    return response.text.strip()

