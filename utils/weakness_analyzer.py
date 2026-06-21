import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def analyze_student(student):

    prompt = f"""
Analyze this student's placement readiness.

Scores:

Aptitude:
{student.aptitude_score}

Coding:
{student.coding_score}

Interview:
{student.interview_score}

Resume:
{student.resume_score}

Provide:

1. Strengths
2. Weaknesses
3. Improvement Areas
4. 30 Day Action Plan
5. Suggested Companies
6. Estimated Placement Readiness
"""

    response = model.generate_content(
        prompt
    )

    return response.text