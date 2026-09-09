def analyze_quiz_performance(records):

    if not records:
        return {
            "status": "No analytics data available",
            "weak_questions": [],
            "average_accuracy": 0
        }

    total_attempts = sum(
        r.attempts for r in records
    )

    total_correct = sum(
        r.correct_answers for r in records
    )

    accuracy = 0

    if total_attempts:
        accuracy = round(
            (total_correct / total_attempts) * 100,
            1
        )

    weak_questions = []

    for r in records:
        if r.accuracy_rate < 50:
            weak_questions.append({
                "question_id": r.question_id,
                "accuracy": r.accuracy_rate
            })

    return {
        "status": "Analysis completed",
        "average_accuracy": accuracy,
        "weak_questions": weak_questions,
        "recommendation": generate_recommendation(accuracy)
    }


def generate_recommendation(accuracy):

    if accuracy < 50:
        return "Recommend easier questions and revision-based Bible study."

    elif accuracy < 75:
        return "Maintain current difficulty and strengthen weak areas."

    else:
        return "Increase difficulty level for advanced learners."
