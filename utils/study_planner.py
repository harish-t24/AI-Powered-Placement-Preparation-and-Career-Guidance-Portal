import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_study_plan(days, role):

    prompt = f"""
Create a detailed placement preparation study plan.

Days Available:
{days}

Target Role:
{role}

Include:

- Aptitude
- DSA
- DBMS
- Operating Systems
- Computer Networks
- OOP
- Mock Interviews
- Resume Preparation

Provide a day-wise roadmap.
"""

    response = model.generate_content(prompt)

    return response.text