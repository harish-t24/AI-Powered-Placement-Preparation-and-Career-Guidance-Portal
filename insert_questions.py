from app import app
from extensions import db
from models.student import AptitudeQuestion

with app.app_context():

    if AptitudeQuestion.query.count() == 0:

        questions = [

            AptitudeQuestion(
                question="2 + 2 = ?",
                option1="2",
                option2="4",
                option3="6",
                option4="8",
                answer="4"
            ),

            AptitudeQuestion(
                question="10 / 2 = ?",
                option1="2",
                option2="5",
                option3="10",
                option4="20",
                answer="5"
            ),

            AptitudeQuestion(
                question="5 * 6 = ?",
                option1="11",
                option2="25",
                option3="30",
                option4="60",
                answer="30"
            ),

            AptitudeQuestion(
                question="Square root of 64?",
                option1="6",
                option2="7",
                option3="8",
                option4="9",
                answer="8"
            ),

            AptitudeQuestion(
                question="15 + 20 = ?",
                option1="25",
                option2="30",
                option3="35",
                option4="40",
                answer="35"
            )

        ]

        db.session.add_all(questions)

        db.session.commit()

        print("Questions inserted.")

    else:

        print("Questions already exist.")