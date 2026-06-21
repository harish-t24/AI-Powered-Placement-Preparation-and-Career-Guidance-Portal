from app import app
from extensions import db
from models.student import CodingQuestion

with app.app_context():

    if CodingQuestion.query.count() == 0:

        questions = [

            CodingQuestion(
                title="Reverse String",
                difficulty="Easy",
                description="""
Write a program to reverse a string.
                """,
                sample_input="hello",
                sample_output="olleh"
            ),

            CodingQuestion(
                title="Factorial",
                difficulty="Easy",
                description="""
Find factorial of a number.
                """,
                sample_input="5",
                sample_output="120"
            ),

            CodingQuestion(
                title="Palindrome Check",
                difficulty="Medium",
                description="""
Check whether a string is palindrome.
                """,
                sample_input="madam",
                sample_output="Palindrome"
            ),

            CodingQuestion(
                title="Fibonacci Series",
                difficulty="Medium",
                description="""
Generate first N Fibonacci numbers.
                """,
                sample_input="5",
                sample_output="0 1 1 2 3"
            )

        ]

        db.session.add_all(questions)

        db.session.commit()

        print("Coding Questions Added")

    else:

        print("Questions Already Exist")