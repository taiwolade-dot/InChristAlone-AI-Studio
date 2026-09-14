def generate_data_alerts(summary):

    alerts = []

    if summary.get("churches", 0) == 0:
        alerts.append({
            "level": "High",
            "title": "No Church Records",
            "message": "Church profiles need to be created."
        })

    if summary.get("members", 0) == 0:
        alerts.append({
            "level": "Medium",
            "title": "Member Data Missing",
            "message": "Member records should be developed."
        })

    if summary.get("pastors", 0) == 0:
        alerts.append({
            "level": "Medium",
            "title": "Leadership Records Missing",
            "message": "Pastor profiles should be completed."
        })

    return alerts


def generate_activity_alerts(summary):

    alerts = []

    if summary.get("events", 0) < 3:
        alerts.append({
            "level": "Low",
            "title": "Low Ministry Activity",
            "message": "Increase recorded ministry activities."
        })

    return alerts


def generate_alert_report(summary):

    return {
        "data_alerts": generate_data_alerts(summary),
        "activity_alerts": generate_activity_alerts(summary)
    }
