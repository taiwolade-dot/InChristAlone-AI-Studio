from models import (
    db,
    QuizQuestionAnalytics,
    QuizAnswer
)

def update_question_analytics(question_id):
    """
    Update analytics for a single question based on all recorded answers.
    """

    analytics = QuizQuestionAnalytics.query.filter_by(
        question_id=question_id
    ).first()

    if analytics is None:
        analytics = QuizQuestionAnalytics(
            question_id=question_id
        )
        db.session.add(analytics)

    answers = QuizAnswer.query.filter_by(
        question_id=question_id
    ).all()

    analytics.times_answered = len(answers)
    analytics.correct_answers = sum(
        1 for a in answers if a.is_correct
    )

    if analytics.times_answered:
        analytics.accuracy_rate = round(
            (analytics.correct_answers / analytics.times_answered) * 100,
            2
        )
    else:
        analytics.accuracy_rate = 0

    analytics.difficulty_score = round(
        100 - analytics.accuracy_rate,
        2
    )

    if analytics.accuracy_rate >= 80:
        analytics.ai_recommendation = "Question is appropriate."
    elif analytics.accuracy_rate >= 50:
        analytics.ai_recommendation = (
            "Moderately difficult. Monitor learner performance."
        )
    else:
        analytics.ai_recommendation = (
            "Very difficult. Consider revising wording or adding explanation."
        )

    db.session.commit()

    return analytics
