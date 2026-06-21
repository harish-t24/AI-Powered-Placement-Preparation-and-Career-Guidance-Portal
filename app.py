from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

from utils.code_reviewer import (
    review_code
)

import subprocess
import tempfile
import os

from utils.ai_questions import (
    generate_interview_question
)

from utils.gemini_interview import (
    evaluate_answer
)

from utils.weakness_analyzer import (
    analyze_student
)

from utils.resume_builder import (
    generate_resume
)

from utils.resume_pdf import (
    create_resume_pdf
)

from flask import send_file

from utils.ai_questions import (
    generate_technical_question
)

from utils.technical_evaluator import (
    evaluate_technical_answer
)

from utils.study_planner import (
    generate_study_plan
)

from utils.career_chat import (
    ask_career_coach
)

from utils.ai_questions import (
    generate_aptitude_questions
)
from utils.ai_questions import (
    generate_coding_questions
)
from flask import send_file
import os

from utils.pdf_report import (
    generate_report
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from utils.gemini_interview import (
    evaluate_answer
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from config import Config

from extensions import (
    db,
    login_manager,
    bcrypt
)

from models.student import (
    Student,
    AptitudeQuestion,
    CodingQuestion,
    Admin
)

from utils.resume_analyzer import (
    extract_text,
    calculate_score
)

from utils.placement_score import (
    calculate_readiness
)

app = Flask(__name__)

app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
with app.app_context():
    db.create_all()
login_manager.init_app(app)
bcrypt.init_app(app)

login_manager.login_view = "login"

# Create Database
with app.app_context():
    db.create_all()

def update_streak(student):

    student.streak += 1

    db.session.commit()


# ==========================
# Flask Login User Loader
# ==========================

@login_manager.user_loader
def load_user(user_id):

    return Student.query.get(int(user_id))


# ==========================
# Home
# ==========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================
# Register
# ==========================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = Student.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        student = Student(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# ==========================
# Login
# ==========================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = Student.query.filter_by(
            email=email
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid Email or Password",
            "danger"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "login.html"
    )


# ==========================
# Logout
# ==========================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
@login_required
def dashboard():

    readiness = calculate_readiness(
        current_user
    )

    placement_probability = calculate_placement_probability(
        current_user
    )

    companies = recommend_companies(
        placement_probability
    )

    badges = get_badges(
        current_user
    )

    return render_template(

        "dashboard.html",

        student=current_user,

        readiness=readiness,

        placement_probability=placement_probability,

        companies=companies,
        
        badges=badges

    )


# ==========================
# Profile
# ==========================

@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        student=current_user
    )


# ==========================
# Aptitude Test
# ==========================

@app.route(
    "/aptitude",
    methods=["GET", "POST"]
)
@login_required
def aptitude():

    questions = AptitudeQuestion.query.all()

    if request.method == "POST":

        score = 0

        for q in questions:

            selected = request.form.get(
                f"question_{q.id}"
            )

            if selected == q.answer:

                score += 1

        current_user.aptitude_score = (
            score * 10
        )

        update_streak(current_user)

        create_notification(

            current_user.id,

            "Interview completed successfully."

        )

        db.session.commit()

        return render_template(
            "aptitude_result.html",
            score=score,
            total=len(questions)
        )

    return render_template(
        "aptitude.html",
        questions=questions
    )


# ==========================
# Coding Practice
# ==========================

@app.route('/coding')
@login_required
def coding():

    questions = CodingQuestion.query.all()

    print("Questions Count:", len(questions))
    print("Questions:", questions)

    return render_template(
        'coding.html',
        questions=questions
    )

@app.route("/run-code", methods=["POST"])
@login_required
def run_code():

    code = request.form.get("code")

    output = "Code executed successfully."

    return render_template(
        "run_result.html",
        code=code,
        output=output
    )

@app.route("/submit-solution", methods=["POST"])
@login_required
def submit_solution():

    student = Student.query.get(current_user.id)

    student.coding_score = min(
        student.coding_score + 25,
        100
    )

    db.session.commit()

    flash("Solution Submitted Successfully!")

    return redirect("/dashboard")

@app.route("/ai-review", methods=["POST"])
@login_required
def ai_review():

    code = request.form.get("code")

    try:
        feedback = review_code(code)
    except Exception as e:
        feedback = f"AI Review Error: {str(e)}"

    return render_template(
        "review_result.html",
        feedback=feedback
    )

# ==========================
# Mock Interview
# ==========================

@app.route(
    "/interview",
    methods=["GET", "POST"]
)
@login_required
def interview():

    from utils.ai_questions import (
    generate_interview_question
)

    question = generate_interview_question()

    if request.method == "POST":

        answer = request.form["answer"]

        ai_feedback = evaluate_answer(
            question,
            answer
        )

        word_count = len(
            answer.split()
        )

        word_count = len(answer.split())

        if word_count >= 100:
            score = 100

        elif word_count >= 75:
            score = 90

        elif word_count >= 50:
            score = 80

        elif word_count >= 30:
            score = 70

        elif word_count >= 15:
            score = 60

        else:
            score = 40

        current_user.interview_score = score

        update_streak(current_user)

        log_activity(

            current_user.id,

            "Completed Mock Interview"

        )

        create_notification(

            current_user.id,

            "Great job completing the aptitude test!"

        )

        db.session.commit()

        return render_template(
            "interview_result.html",
            feedback=ai_feedback,
            score=score
        )

    return render_template(
        "interview.html",
        question=question
    )


# ==========================
# Resume Analyzer
# ==========================

@app.route(
    "/resume",
    methods=["GET", "POST"]
)
@login_required
def resume():

    if request.method == "POST":

        pdf_file = request.files["resume"]

        text = extract_text(
            pdf_file
        )

        score, skills = calculate_score(
            text
        )

        current_user.resume_score = score

        db.session.commit()

        return render_template(
            "resume_result.html",
            score=score,
            skills=skills
        )

    return render_template(
        "resume.html"
    )

# ==========================
# Admin Dashboard
# ==========================

@app.route("/admin")
def admin():

    students = Student.query.all()

    total_students = len(students)

    if total_students == 0:

        total_students = 1

    avg_aptitude = sum(
        s.aptitude_score
        for s in students
    ) / total_students

    avg_coding = sum(
        s.coding_score
        for s in students
    ) / total_students

    avg_interview = sum(
        s.interview_score
        for s in students
    ) / total_students

    avg_resume = sum(
        s.resume_score
        for s in students
    ) / total_students

    return render_template(

        "admin.html",

        students=students,

        total_students=len(students),

        avg_aptitude=round(avg_aptitude,2),

        avg_coding=round(avg_coding,2),

        avg_interview=round(avg_interview,2),

        avg_resume=round(avg_resume,2)

    )


# ==========================
# Add Aptitude Question
# ==========================

@app.route(
    "/admin/add-aptitude",
    methods=["GET", "POST"]
)
def add_aptitude():

    if request.method == "POST":

        question = request.form["question"]

        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]

        answer = request.form["answer"]

        q = AptitudeQuestion(

            question=question,

            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,

            answer=answer
        )

        db.session.add(q)
        db.session.commit()

        return redirect("/admin")

    return render_template(
        "add_aptitude.html"
    )

from flask import send_file
import os

from flask import send_file
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime


@app.route("/download-report")
@login_required
def download_report():

    filename = f"report_{current_user.id}.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    content = []

    # ==========================
    # Header
    # ==========================

    content.append(
        Paragraph(
            "AI PLACEMENT PERFORMANCE REPORT",
            title_style
        )
    )

    content.append(
        Paragraph(
            "AI-Powered Placement Preparation & Career Guidance Portal",
            styles["Heading3"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==========================
    # Student Details
    # ==========================

    content.append(
        Paragraph(
            "Student Information",
            heading_style
        )
    )

    student_data = [
        ["Name", current_user.name],
        ["Email", current_user.email],
        ["Report Date", datetime.now().strftime("%d-%m-%Y")]
    ]

    student_table = Table(
        student_data,
        colWidths=[120, 320]
    )

    student_table.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(0,-1),colors.darkblue),
            ('TEXTCOLOR',(0,0),(0,-1),colors.white),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold')
        ])
    )

    content.append(student_table)

    content.append(
        Spacer(1,20)
    )

    # ==========================
    # Scores
    # ==========================

    aptitude = getattr(
        current_user,
        "aptitude_score",
        0
    )

    coding = getattr(
        current_user,
        "coding_score",
        0
    )

    interview = getattr(
        current_user,
        "interview_score",
        0
    )

    resume = getattr(
        current_user,
        "resume_score",
        0
    )

    readiness = round(
        calculate_readiness(current_user),
        1
    )

    content.append(
        Paragraph(
            "Performance Summary",
            heading_style
        )
    )

    score_data = [
        ["Assessment", "Score"],
        ["Aptitude", aptitude],
        ["Coding", coding],
        ["Interview", interview],
        ["Resume", resume],
        ["Placement Readiness", f"{readiness}%"]
    ]

    score_table = Table(
        score_data,
        colWidths=[250,150]
    )

    score_table.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1e40af")),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke)
        ])
    )

    content.append(score_table)

    content.append(
        Spacer(1,20)
    )

    # ==========================
    # Readiness Section
    # ==========================

    content.append(
        Paragraph(
            f"""
            <para align='center'>
            <font size='20' color='green'>
            Placement Readiness Score: {readiness}%
            </font>
            </para>
            """,
            normal_style
        )
    )

    content.append(
        Spacer(1,20)
    )

    # ==========================
    # AI Recommendation
    # ==========================

    recommendation = ""

    if readiness >= 90:
        recommendation = """
        Excellent performance. You are highly placement-ready and
        can confidently attend campus interviews.
        """

    elif readiness >= 75:
        recommendation = """
        Good performance. Improve coding and mock interview practice
        to maximize placement chances.
        """

    else:
        recommendation = """
        More preparation is required. Focus on aptitude,
        coding challenges, and resume improvement.
        """

    content.append(
        Paragraph(
            "AI Recommendation",
            heading_style
        )
    )

    content.append(
        Paragraph(
            recommendation,
            normal_style
        )
    )

    content.append(
        Spacer(1,40)
    )

    # ==========================
    # Footer
    # ==========================

    content.append(
        Paragraph(
            """
            <para align='center'>
            <font size='10'>
            Generated Automatically by AI Placement Portal
            <br/>
            © 2026 AI Placement Preparation & Career Guidance Portal
            </font>
            </para>
            """,
            normal_style
        )
    )

    doc.build(content)

    return send_file(
        filename,
        as_attachment=True,
        download_name="AI_Placement_Report.pdf"
    )

from flask import send_file
from flask_login import login_required, current_user
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from datetime import datetime


@app.route("/certificate")
@login_required
def certificate():

    readiness = round(
        calculate_readiness(current_user),
        1
    )

    if readiness < 80:
        return """
        <div style="text-align:center;margin-top:100px;font-family:Arial;">
            <h1>🏆 Certificate Locked</h1>
            <h3>Minimum Readiness Score Required: 80%</h3>
            <h2>Keep Practicing!</h2>
        </div>
        """

    aptitude = getattr(current_user, "aptitude_score", 0)
    coding = getattr(current_user, "coding_score", 0)
    interview = getattr(current_user, "interview_score", 0)
    resume = getattr(current_user, "resume_score", 0)

    cert_id = f"AIPP-{datetime.now().year}-{current_user.id:04d}"

    filename = f"certificate_{current_user.id}.pdf"

    c = canvas.Canvas(
        filename,
        pagesize=landscape(A4)
    )

    width, height = landscape(A4)

    # ==========================
    # Background
    # ==========================

    c.setFillColorRGB(0.06, 0.13, 0.42)
    c.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    # ==========================
    # Outer Border
    # ==========================

    c.setStrokeColor(colors.gold)
    c.setLineWidth(8)

    c.rect(
        20,
        20,
        width - 40,
        height - 40
    )

    c.setLineWidth(2)

    c.rect(
        35,
        35,
        width - 70,
        height - 70
    )

    # ==========================
    # Header
    # ==========================

    c.setFillColor(colors.white)

    c.setFont(
        "Helvetica-Bold",
        18
    )

    c.drawCentredString(
        width / 2,
        height - 50,
        "AI PLACEMENT PORTAL"
    )

    # ==========================
    # Title
    # ==========================

    c.setFillColor(colors.gold)

    c.setFont(
        "Helvetica-Bold",
        32
    )

    c.drawCentredString(
        width / 2,
        height - 110,
        "CERTIFICATE OF EXCELLENCE"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawCentredString(
        width / 2,
        height - 135,
        f"Certificate ID : {cert_id}"
    )

    # ==========================
    # Award
    # ==========================

    if readiness >= 95:
        award = "PLATINUM ACHIEVEMENT AWARD"
    elif readiness >= 85:
        award = "GOLD ACHIEVEMENT AWARD"
    else:
        award = "SILVER ACHIEVEMENT AWARD"

    c.setFont(
        "Helvetica-Bold",
        18
    )

    c.drawCentredString(
        width / 2,
        height - 185,
        award
    )

    # ==========================
    # Gold Badge
    # ==========================

    c.setFillColor(colors.gold)

    c.circle(
        width - 140,
        height - 220,
        35,
        fill=1
    )

    c.setFillColor(colors.black)

    c.setFont(
        "Helvetica-Bold",
        9
    )

    c.drawCentredString(
        width - 140,
        height - 215,
        "TOP"
    )

    c.drawCentredString(
        width - 140,
        height - 228,
        "CANDIDATE"
    )

    # ==========================
    # Main Text
    # ==========================

    c.setFillColor(colors.white)

    c.setFont(
        "Helvetica",
        18
    )

    c.drawCentredString(
        width / 2,
        height - 250,
        "This Certificate is Proudly Awarded To"
    )

    c.setFillColor(colors.gold)

    c.setFont(
        "Helvetica-Bold",
        30
    )

    c.drawCentredString(
        width / 2,
        height - 310,
        current_user.name.upper()
    )

    c.setFillColor(colors.white)

    c.setFont(
        "Helvetica",
        17
    )

    c.drawCentredString(
        width / 2,
        height - 360,
        "For Successfully Completing"
    )

    c.setFont(
        "Helvetica-Bold",
        20
    )

    c.drawCentredString(
        width / 2,
        height - 395,
        "AI-Powered Placement Preparation"
    )

    c.drawCentredString(
        width / 2,
        height - 425,
        "and Career Guidance Program"
    )

    # ==========================
    # Readiness Score
    # ==========================

    c.setFillColor(colors.gold)

    c.setFont(
        "Helvetica-Bold",
        24
    )

    c.drawCentredString(
        width / 2,
        height - 485,
        f"Placement Readiness Score : {readiness}%"
    )

    # ==========================
    # Achievement Line
    # ==========================

    c.setFillColor(colors.gold)

    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawCentredString(
        width / 2,
        70,
        "TOP PLACEMENT READY CANDIDATE"
    )

    # ==========================
    # Date
    # ==========================

    c.setFillColor(colors.white)

    c.setFont(
        "Helvetica",
        11
    )

    c.drawString(
        60,
        45,
        f"Issue Date : {datetime.now().strftime('%d-%m-%Y')}"
    )

    # ==========================
    # Verified
    # ==========================

    c.setFillColor(colors.green)

    c.setFont(
        "Helvetica-Bold",
        13
    )

    c.drawRightString(
        width - 60,
        45,
        "✓ VERIFIED"
    )

    # ==========================
    # Footer
    # ==========================

    c.setFillColor(colors.white)

    c.setFont(
        "Helvetica-Oblique",
        8
    )

    c.drawCentredString(
        width / 2,
        25,
        "This certificate is digitally generated and verified by AI Placement Portal."
    )

    c.save()

    return send_file(
        filename,
        as_attachment=True,
        download_name=f"{current_user.name}_Certificate.pdf"
    )

from flask import session

@app.route(
    "/ai-aptitude",
    methods=["GET", "POST"]
)
@login_required
def ai_aptitude():

    if request.method == "POST":

        if "generate" in request.form:

            difficulty = request.form[
                "difficulty"
            ]

            company = request.form[
                "company"
            ]

            questions = generate_aptitude_questions(
                difficulty,
                company
            )

            session[
                "aptitude_questions"
            ] = questions

            return render_template(
                "ai_aptitude_test.html",
                questions=questions
            )

        elif "submit_test" in request.form:

            questions = session.get(
                "aptitude_questions",
                []
            )

            score = 0

            for i, q in enumerate(
                questions
            ):

                selected = request.form.get(
                    f"q{i}"
                )

                if selected == q["answer"]:

                    score += 1

            current_user.aptitude_score = (
                score * 10
            )

            update_streak(current_user)

            save_performance(
                current_user
            )

            log_activity(

                current_user.id,

                "Completed AI Aptitude Test"

            )

            create_notification(

                current_user.id,

                "Interview completed successfully."

            )

            db.session.commit()

            return render_template(
                "ai_aptitude_result.html",
                score=score,
                total=len(questions)
            )

    return render_template(
        "ai_aptitude_setup.html"
    )

@app.route(
    "/ai-coding",
    methods=["GET", "POST"]
)
@login_required
def ai_coding():

    if request.method == "POST":

        language = request.form["language"]

        difficulty = request.form["difficulty"]

        company = request.form["company"]

        questions = generate_coding_questions(
            language,
            difficulty,
            company
        )

        update_streak(current_user)

        save_performance(
            current_user
        )

        log_activity(

            current_user.id,

            "Generated AI Coding Questions"

        )

        create_notification(

            current_user.id,

            "New coding questions generated."

        )

        return render_template(
            "ai_coding_result.html",
            questions=questions
        )

    return render_template(
        "ai_coding_setup.html"
    )

@app.route(
    "/career-chat",
    methods=["GET", "POST"]
)
@login_required
def career_chat():

    reply = None

    if request.method == "POST":

        question = request.form["question"]

        reply = ask_career_coach(question)

    log_activity(

        current_user.id,

        "Used Career Coach"

    )

    return render_template(
        "career_chat.html",
        reply=reply
    )

def calculate_placement_probability(student):

    probability = (

        student.aptitude_score * 0.25 +

        student.coding_score * 0.35 +

        student.interview_score * 0.25 +

        student.resume_score * 0.15

    )

    return round(probability)

def recommend_companies(probability):

    if probability >= 85:

        return [
            "Google",
            "Amazon",
            "Microsoft",
            "Zoho"
        ]

    elif probability >= 70:

        return [
            "Zoho",
            "Infosys",
            "TCS",
            "Accenture"
        ]

    else:

        return [
            "TCS",
            "Wipro",
            "Cognizant"
        ]

@app.route(
    "/study-planner",
    methods=["GET", "POST"]
)
@login_required
def study_planner():

    plan = None

    if request.method == "POST":

        days = request.form["days"]

        role = request.form["role"]

        plan = generate_study_plan(
            days,
            role
        )

        update_streak(current_user)

    return render_template(
        "study_planner.html",
        plan=plan
    )

@app.route(
    "/technical-interview",
    methods=["GET", "POST"]
)
@login_required
def technical_interview():

    if request.method == "POST":

        if "generate" in request.form:

            subject = request.form["subject"]

            question = generate_technical_question(
                subject
            )

            session["technical_subject"] = subject
            session["technical_question"] = question

            return render_template(
                "technical_question.html",
                subject=subject,
                question=question
            )

        elif "submit_answer" in request.form:

            subject = session.get(
                "technical_subject"
            )

            question = session.get(
                "technical_question"
            )

            answer = request.form["answer"]

            feedback = evaluate_technical_answer(
                subject,
                question,
                answer
            )

            update_streak(current_user)

            save_performance(
                current_user
            )

            log_activity(

                current_user.id,

                "Completed Technical Interview"

            )

            return render_template(
                "technical_result.html",
                feedback=feedback
            )

    return render_template(
        "technical_setup.html"
    )

@app.route("/leaderboard")
@login_required
def leaderboard():

    students = Student.query.order_by(

        (
            Student.aptitude_score +
            Student.coding_score +
            Student.interview_score +
            Student.resume_score

        ).desc()

    ).all()

    return render_template(
        "leaderboard.html",
        students=students
    )

@app.route(
    "/resume-builder",
    methods=["GET","POST"]
)
@login_required
def resume_builder():

    if request.method == "POST":

        name = request.form["name"]

        role = request.form["role"]

        skills = request.form["skills"]

        projects = request.form["projects"]

        education = request.form["education"]

        resume_content = generate_resume(

            name,
            role,
            skills,
            projects,
            education

        )

        filepath = (
            f"reports/resume_{current_user.id}.pdf"
        )

        create_resume_pdf(
            resume_content,
            filepath
        )

        log_activity(

            current_user.id,

            "Generated Resume"

        )

        return send_file(
            filepath,
            as_attachment=True
        )

    return render_template(
        "resume_builder.html"
    )

@app.route("/weakness-analysis")
@login_required
def weakness_analysis():

    report = analyze_student(
        current_user
    )

    return render_template(
        "weakness_analysis.html",
        report=report
    )

@app.route(
    "/browser-voice-interview",
    methods=["GET", "POST"]
)
@login_required
def browser_voice_interview():

    if request.method == "POST":

        question = request.form["question"]

        answer = request.form["answer"]

        feedback = evaluate_answer(
            question,
            answer
        )

        return render_template(
            "voice_result.html",
            question=question,
            answer=answer,
            feedback=feedback
        )

    question = generate_interview_question()

    return render_template(
        "browser_voice_interview.html",
        question=question
    )

@app.route("/code-compiler", methods=["GET", "POST"])
@login_required
def code_compiler():

    output = ""
    review = ""

    if request.method == "POST":

        code = request.form["code"]

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".py",
                mode="w",
                encoding="utf-8"
            ) as f:

                f.write(code)

                filename = f.name

            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True,
                timeout=5
            )

            output = (
                result.stdout
                if result.stdout
                else result.stderr
            )

            review = review_code(code)

            os.unlink(filename)

        except Exception as e:

            output = str(e)

    return render_template(
        "code_compiler.html",
        output=output,
        review=review
    )

def get_badges(student):

    badges = []

    if student.aptitude_score >= 80:
        badges.append(
            "🧠 Aptitude Master"
        )

    if student.coding_score >= 80:
        badges.append(
            "💻 Coding Champion"
        )

    if student.interview_score >= 80:
        badges.append(
            "🎤 Interview Expert"
        )

    if student.resume_score >= 80:
        badges.append(
            "📄 Resume Pro"
        )

    avg = (

        student.aptitude_score +

        student.coding_score +

        student.interview_score +

        student.resume_score

    ) / 4

    if avg >= 75:
        badges.append(
            "🏆 Placement Ready"
        )

    if student.streak >= 5:

        badges.append(
            "🔥 5 Day Warrior"
        )

    if student.streak >= 15:

        badges.append(
            "🚀 Consistency Star"
        )

    if student.streak >= 30:

        badges.append(
            "🏅 Placement Grinder"
        )

    return badges

@app.route("/progress")
@login_required
def progress():

    readiness = calculate_readiness(
        current_user
    )

    return render_template(
        "progress.html",
        readiness=readiness
    )

@app.route("/leaderboard_page")
@login_required
def leaderboard_page():

    students = Student.query.all()

    ranked_students = sorted(

        students,

        key=lambda s: (
            s.aptitude_score +
            s.coding_score +
            s.interview_score +
            s.resume_score
        ),

        reverse=True

    )

    return render_template(
        "leaderboard_page.html",
        students=ranked_students
    )

class Activity(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer
    )

    activity = db.Column(
        db.String(200)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

def log_activity(
    student_id,
    text
):

    activity = Activity(

        student_id=student_id,

        activity=text

    )

    db.session.add(
        activity
    )

    db.session.commit()

@app.route("/activity-history")
@login_required
def activity_history():

    activities = Activity.query.filter_by(

        student_id=current_user.id

    ).order_by(

        Activity.created_at.desc()

    ).all()

    return render_template(

        "activity_history.html",

        activities=activities

    )

def save_performance(student):

    readiness = calculate_readiness(
        student
    )

    record = PerformanceHistory(

        student_id=student.id,

        aptitude=student.aptitude_score,

        coding=student.coding_score,

        interview=student.interview_score,

        resume=student.resume_score,

        readiness=readiness

    )

    db.session.add(record)

    db.session.commit()

@app.route("/performance")
@login_required
def performance():

    history = PerformanceHistory.query.filter_by(

        student_id=current_user.id

    ).all()

    labels = []

    readiness_scores = []

    for item in history:

        labels.append(
            item.created_at.strftime(
                "%d-%m"
            )
        )

        readiness_scores.append(
            item.readiness
        )

    return render_template(

        "performance.html",

        labels=labels,

        readiness_scores=readiness_scores

    )

class PerformanceHistory(db.Model):
    __tablename__ = "performance_history"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)

    aptitude = db.Column(db.Integer, default=0)
    coding = db.Column(db.Integer, default=0)
    interview = db.Column(db.Integer, default=0)
    resume = db.Column(db.Integer, default=0)

    readiness = db.Column(db.Float, default=0)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    message = db.Column(db.String(500))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

def create_notification(
    student_id,
    message
):

    notification = Notification(

        student_id=student_id,

        message=message

    )

    db.session.add(
        notification
    )

    db.session.commit()

@app.route("/notifications")
@login_required
def notifications():

    notifications = Notification.query.filter_by(

        student_id=current_user.id

    ).order_by(

        Notification.created_at.desc()

    ).all()

    return render_template(

        "notifications.html",

        notifications=notifications

    )

@app.route("/delete-user/<int:id>")
def delete_user(id):

    student = Student.query.get(id)

    if student:

        db.session.delete(student)
        db.session.commit()

    return redirect("/admin")

@app.route("/view-student/<int:id>")
def view_student(id):

    student = Student.query.get(id)

    return render_template(
        "student_view.html",
        student=student
    )

from flask import Response
import csv
import io


@app.route("/export-students")
def export_students():

    students = Student.query.all()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Name",
        "Email",
        "Aptitude",
        "Coding",
        "Interview",
        "Resume"
    ])

    for student in students:

        writer.writerow([

            student.id,
            student.name,
            student.email,
            student.aptitude_score,
            student.coding_score,
            student.interview_score,
            student.resume_score

        ])

    output.seek(0)

    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=students.csv"
        }

    )

with app.app_context():
    db.create_all()

# ==========================
# Run Application
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )