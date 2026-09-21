from datetime import datetime

def seconds_remaining(session):
    """
    Returns the number of seconds remaining for the current question.
    """
    if session.question_started_at is None:
        return session.seconds_per_question

    elapsed = int(
        (datetime.utcnow() - session.question_started_at).total_seconds()
    )

    return max(0, session.seconds_per_question - elapsed)
