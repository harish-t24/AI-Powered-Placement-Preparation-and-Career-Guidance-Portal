import PyPDF2

skills = [

    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "django",
    "machine learning",
    "git",
    "github"

]


def extract_text(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text

    return text


def calculate_score(text):

    score = 0

    detected_skills = []

    for skill in skills:

        if skill.lower() in text.lower():

            score += 8

            detected_skills.append(skill)

    score = min(score, 100)

    return score, detected_skills