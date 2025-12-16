# utils/llm.py — Gemini (polished answers)

import os
from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# ENV + GEMINI CONFIG
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash"

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = """
You are ALVIN, the official AI assistant of the Mohammed VI Library at Al Akhawayn University.

Your task:
- Rewrite the provided library answer in a FORMAL tone
- Use CLEAR BULLET POINTS
- Lightly rephrase (do NOT invent information)
- Do NOT add new facts
- Be concise and professional

Always end the answer with:
"If you need further assistance, please contact the library at researchandlearning@aui.ma."

If no reliable answer is provided, say you are not fully sure and suggest contacting the library.
""".strip()

# -----------------------------
# GENERATE POLISHED ANSWER
# -----------------------------
def generate_answer(raw_answer: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

Original library answer:
{raw_answer}

Rewrite the answer now.
""".strip()

    try:
        response = genai.GenerativeModel(MODEL).generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 300
            }
        )

        return response.text.strip()

    except Exception:
        return (
            "• We are currently unable to generate a refined response.\n"
            "• Please contact the library directly at researchandlearning@aui.ma."
        )
