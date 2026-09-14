def generate_ministry_insights(summary):

    insights = []

    if summary["churches"] == 0:
        insights.append(
            "No church records found. Add church profiles to improve ministry intelligence."
        )
    else:
        insights.append(
            f"{summary['churches']} church profile(s) are currently registered."
        )

    if summary["pastors"] == 0:
        insights.append(
            "No pastor profiles detected. Complete pastor records for leadership intelligence."
        )
    else:
        insights.append(
            f"{summary['pastors']} pastor profile(s) are available."
        )

    if summary["quiz_accuracy"] >= 80:
        insights.append(
            "Bible Quiz learning performance is excellent."
        )
    elif summary["quiz_accuracy"] >= 50:
        insights.append(
            "Bible Quiz performance is moderate. Consider additional teaching support."
        )
    else:
        insights.append(
            "Bible Quiz performance requires attention and discipleship support."
        )

    if summary["events"] > 0:
        insights.append(
            f"{summary['events']} ministry event(s) recorded in the calendar."
        )
    else:
        insights.append(
            "No ministry events recorded. Consider planning upcoming activities."
        )

    return insights
