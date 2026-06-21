from flask_login import UserMixin
from extensions import db


# ==========================
# Student Model
# ==========================

class Student(UserMixin, db.Model):

    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    aptitude_score = db.Column(
        db.Integer,
        default=0
    )

    coding_score = db.Column(
        db.Integer,
        default=0
    )

    interview_score = db.Column(
        db.Integer,
        default=0
    )

    resume_score = db.Column(
        db.Integer,
        default=0
    )

    streak = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):
        return f"<Student {self.name}>"



# ==========================
# Aptitude Questions
# ==========================

class AptitudeQuestion(db.Model):

    __tablename__ = "aptitude_questions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.String(500),
        nullable=False
    )

    option1 = db.Column(
        db.String(200),
        nullable=False
    )

    option2 = db.Column(
        db.String(200),
        nullable=False
    )

    option3 = db.Column(
        db.String(200),
        nullable=False
    )

    option4 = db.Column(
        db.String(200),
        nullable=False
    )

    answer = db.Column(
        db.String(200),
        nullable=False
    )



# ==========================
# Coding Questions
# ==========================

class CodingQuestion(db.Model):

    __tablename__ = "coding_questions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    difficulty = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    sample_input = db.Column(
        db.Text
    )

    sample_output = db.Column(
        db.Text
    )



# ==========================
# Admin Model
# ==========================

class Admin(db.Model):

    __tablename__ = "admins"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )