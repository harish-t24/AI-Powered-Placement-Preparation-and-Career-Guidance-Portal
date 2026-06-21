import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def ask_career_coach(message):

    prompt = f"""
You are an AI Career Coach.

Help students with:

- Placement preparation
- Aptitude
- Coding
- Resume building
- Interview preparation
- Career guidance
- Roadmaps

Student Question:

{message}
"""

    response = model.generate_content(
        prompt
    )

    return response.text