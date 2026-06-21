import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_resume(
    name,
    role,
    skills,
    projects,
    education
):

    prompt = f"""
Create a professional ATS-friendly resume.

Name:
{name}

Target Role:
{role}

Skills:
{skills}

Projects:
{projects}

Education:
{education}

Format professionally.
"""

    response = model.generate_content(
        prompt
    )

    return response.text