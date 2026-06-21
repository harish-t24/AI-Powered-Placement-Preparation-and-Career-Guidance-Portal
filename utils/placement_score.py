def calculate_readiness(student):

    scores = [

        student.aptitude_score,
        student.coding_score,
        student.interview_score,
        student.resume_score

    ]

    total = sum(scores)

    readiness = total / 4

    return round(readiness, 2)