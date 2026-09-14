def calculate_ministry_health(summary):

    score = 0

    if summary["churches"] > 0:
        score += 20

    if summary["members"] > 0:
        score += 20

    if summary["events"] > 0:
        score += 20

    if summary["quiz_participants"] > 0:
        score += 20

    if summary["quiz_accuracy"] >= 50:
        score += 20

    return score
