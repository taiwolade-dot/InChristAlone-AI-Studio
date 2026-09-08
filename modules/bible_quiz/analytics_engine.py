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
            "Consider increasing difficulty level."
        )

    if accuracy_rate <= 40:
        return (
            "Question may require teaching reinforcement "
            "or simpler wording."
        )

    if difficulty_score >= 80:
        return (
            "High difficulty detected. "
            "Consider reviewing biblical concepts."
        )

    return (
        "Question performance is balanced. "
        "Suitable for current target group."
    )
