import google.generativeai as genai
import json

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_aptitude_questions(
    difficulty,
    company
):

    prompt = f"""
Generate 10 aptitude MCQs.

Difficulty: {difficulty}
Company: {company}

Return ONLY valid JSON.

Format:

[
  {{
    "question":"Question",
    "options":["A","B","C","D"],
    "answer":"A"
  }}
]
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)


def generate_coding_questions(
    language,
    difficulty,
    company
):

    prompt = f"""
Generate 10 coding interview questions.

Language: {language}
Difficulty: {difficulty}
Company: {company}

Return HTML only.

For each question provide:

<h3>Title</h3>

<p>Problem Statement</p>

<h5>Sample Input</h5>

<pre>input</pre>

<h5>Sample Output</h5>

<pre>output</pre>

No markdown.
"""

    response = model.generate_content(
        prompt
    )

    return response.text

def generate_interview_question():

    prompt = """
Generate ONE professional HR interview question.

Return only the question.
"""

    response = model.generate_content(
        prompt
    )

    return response.text

def generate_technical_question(subject):

    prompt = f"""
Generate ONE technical interview question.

Subject:
{subject}

Return only the question.
"""

    response = model.generate_content(prompt)

    return response.text