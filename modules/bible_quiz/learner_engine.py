from models import (
    db,
    QuizLearnerProfile,
    QuizAnswer
)


def update_learner_profile(participant_id):

    answers = QuizAnswer.query.filter_by(
        participant_id=participant_id
    ).all()


    if not answers:
        return None


    total = len(answers)

    correct = len([
        a for a in answers
        if a.is_correct
    ])


    accuracy = round(
        (correct / total) * 100,
        1
    )


    if accuracy < 40:

        level = "Beginner"

        recommendation = (
            "Focus on Bible foundations, "
            "memory verses, and revision questions."
        )


    elif accuracy < 75:

        level = "Intermediate"

        recommendation = (
            "Continue structured Bible study "
            "and strengthen weaker areas."
        )


    else:

        level = "Advanced"

        recommendation = (
            "Explore deeper theological questions "
            "and leadership applications."
        )


    profile = QuizLearnerProfile.query.filter_by(
        participant_id=participant_id
    ).first()


    if not profile:

        profile = QuizLearnerProfile(
            participant_id=participant_id
        )

        db.session.add(profile)


    profile.total_questions = total
    profile.correct_answers = correct
    profile.accuracy_rate = accuracy
    profile.learning_level = level
    profile.ai_recommendation = recommendation


    db.session.commit()


    return profile
