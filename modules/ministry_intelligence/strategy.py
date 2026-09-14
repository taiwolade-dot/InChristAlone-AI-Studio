def generate_immediate_actions(alert_report):

    actions = []

    for alert in alert_report.get("data_alerts", []):

        actions.append(
            {
                "priority": alert["level"],
                "action": alert["message"]
            }
        )

    for alert in alert_report.get("activity_alerts", []):

        actions.append(
            {
                "priority": alert["level"],
                "action": alert["message"]
            }
        )

    return actions


def generate_growth_actions(prediction_report):

    actions = []

    growth = prediction_report.get(
        "growth_forecast",
        {}
    )

    if growth.get("direction") == "Positive":

        actions.append(
            "Maintain current ministry growth practices and strengthen engagement."
        )

    else:

        actions.append(
            "Develop targeted ministry growth initiatives."
        )

    return actions


def generate_strategy_report(
    prediction_report,
    alert_report
):

    return {
        "immediate_actions": generate_immediate_actions(
            alert_report
        ),
        "growth_actions": generate_growth_actions(
            prediction_report
        )
    }
