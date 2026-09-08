def generate_recommendation(
    accuracy_rate,
    times_answered,
    difficulty_score
):
    """
    AI adaptive recommendation engine
    """

    if times_answered < 3:
        return (
            "Insufficient data. Continue collecting responses "
            "before adjusting this question."
        )

    if accuracy_rate >= 90:
        return (
            "Question appears too easy. "
            "AI recommends increasing difficulty "
            "or introducing deeper application questions."
        )

    if accuracy_rate <= 40:
        return (
            "Weak learning area detected. "
            "AI recommends Bible teaching reinforcement "
            "and simplified follow-up questions."
        )

    if difficulty_score >= 80:
        return (
            "High difficulty detected. "
            "AI recommends reviewing biblical concepts "
            "before reassessment."
        )

    return (
        "Question performance is balanced. "
        "Suitable for the current target group."
    )



def analyze_quiz_performance(analytics_records):
    """
    Analyze complete quiz performance
    and identify learning gaps.
    """

    weak_questions = []
    strong_questions = []

    for item in analytics_records:

        if item.accuracy_rate <= 40:
            weak_questions.append({
                "question_id": item.question_id,
                "accuracy": item.accuracy_rate,
                "recommendation":
                    "Generate reinforcement questions"
            })


        if item.accuracy_rate >= 90:
            strong_questions.append({
                "question_id": item.question_id,
                "accuracy": item.accuracy_rate,
                "recommendation":
                    "Increase complexity"
            })


    return {
        "weak_questions": weak_questions,
        "strong_questions": strong_questions,
        "total_questions": len(analytics_records)
    }
