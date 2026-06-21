import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def evaluate_technical_answer(
    subject,
    question,
    answer
):

    prompt = f"""
You are a technical interviewer.

Subject:
{subject}

Question:
{question}

Candidate Answer:
{answer}

Provide:

1. Score out of 100
2. Strengths
3. Weaknesses
4. Correct Concepts
5. Suggestions
"""

    response = model.generate_content(
        prompt
    )

    return response.text