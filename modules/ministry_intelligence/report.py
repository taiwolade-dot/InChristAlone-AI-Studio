def generate_executive_summary(summary):

    return {
        "churches": summary.get("churches", 0),
        "members": summary.get("members", 0),
        "pastors": summary.get("pastors", 0),
        "events": summary.get("events", 0),
        "message": (
            "This report provides an overview of current ministry "
            "operations and leadership intelligence."
        )
    }


def generate_intelligence_summary(
    health_score,
    network_report,
    prediction_report
):

    return {
        "health_score": health_score,
        "network": network_report,
        "forecast": prediction_report
    }


def generate_action_summary(
    alert_report,
    strategy_report
):

    return {
        "alerts": alert_report,
        "strategies": strategy_report
    }


def generate_ministry_report(
    summary,
    health_score,
    network_report,
    prediction_report,
    alert_report,
    strategy_report
):

    return {
        "executive_summary": generate_executive_summary(
            summary
        ),
        "intelligence_summary": generate_intelligence_summary(
            health_score,
            network_report,
            prediction_report
        ),
        "action_summary": generate_action_summary(
            alert_report,
            strategy_report
        )
    }
