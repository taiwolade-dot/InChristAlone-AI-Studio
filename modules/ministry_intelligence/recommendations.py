def generate_ministry_recommendations(summary, analytics):

    recommendations = []

    if summary["pastors"] == 0:
        recommendations.append(
            "Complete pastor profiles to strengthen leadership intelligence."
        )

    if summary["members"] < 10:
        recommendations.append(
            "Membership records are limited. Consider improving member registration and follow-up."
        )

    if summary["events"] == 0:
        recommendations.append(
            "No ministry events detected. Develop a structured ministry activity plan."
        )
    else:
        recommendations.append(
            f"{summary['events']} ministry event(s) recorded. Maintain consistent ministry engagement."
        )

    if summary["quiz_accuracy"] < 80:
        recommendations.append(
            "Bible learning performance can improve through additional discipleship support."
        )

    return recommendations
