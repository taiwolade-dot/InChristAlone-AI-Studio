def generate_health_insights(summary):

    strengths = []
    attention = []
    priorities = []

    if summary["churches"] > 0:
        strengths.append(
            "Church profile information is available."
        )
    else:
        attention.append(
            "No church records found."
        )

    if summary["members"] > 0:
        strengths.append(
            "Member records are available."
        )
    else:
        attention.append(
            "Member records need to be developed."
        )

    if summary["events"] > 0:
        strengths.append(
            "Ministry activities are being recorded."
        )
    else:
        attention.append(
            "No ministry events recorded."
        )

    if summary["quiz_participants"] > 0:
        strengths.append(
            "Bible learning participation is active."
        )
    else:
        attention.append(
            "Bible learning participation needs attention."
        )

    if summary["quiz_accuracy"] >= 80:
        strengths.append(
            "Bible learning performance is excellent."
        )
    else:
        attention.append(
            "Bible learning performance can improve."
        )

    if summary["pastors"] == 0:
        priorities.append(
            "Complete pastor profiles to strengthen leadership intelligence."
        )

    if summary["quiz_accuracy"] < 80:
        priorities.append(
            "Strengthen discipleship and teaching support."
        )

    if summary["events"] < 3:
        priorities.append(
            "Increase structured ministry activities."
        )

    return {
        "strengths": strengths,
        "attention": attention,
        "priorities": priorities
    }
