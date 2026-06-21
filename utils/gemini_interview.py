import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def evaluate_answer(
    question,
    answer
):

    prompt = f"""
You are an HR Interview Evaluator.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer and provide:

1. Score out of 100
2. Strengths
3. Weaknesses
4. Suggestions for improvement

Format the response clearly.
"""

    response = model.generate_content(
        prompt
    )

    return response.text