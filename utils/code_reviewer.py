import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def review_code(code):

    prompt = f"""
You are an expert coding interviewer.

Review this code:

{code}

Provide:

1. Correctness
2. Time Complexity
3. Space Complexity
4. Code Quality
5. Improvements
6. Score out of 100

Format nicely.
"""

    response = model.generate_content(
        prompt
    )

    return response.text