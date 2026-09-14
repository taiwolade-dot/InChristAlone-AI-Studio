def generate_ministry_decision_guidance(question):

    q = question.lower()

    decision_explanations = []
    strategic_guidance = []
    recommended_actions = []
    scenario_answers = []
    leadership_insights = []

    if "risk" in q:
        decision_explanations.append(
            "Ministry risks should be identified early through evaluation, data, and leadership reflection."
        )

    if "growth" in q:
        decision_explanations.append(
            "Sustainable ministry growth requires member engagement, leadership development, and strategic planning."
        )

    strategic_guidance.extend([
        "Use ministry data to support prayerful and informed decisions.",
        "Align strategies with mission, vision, and measurable objectives."
    ])

    recommended_actions.extend([
        "Review ministry indicators regularly.",
        "Document lessons learned for future improvement."
    ])

    scenario_answers.extend([
        "Different ministry scenarios should be evaluated before major decisions are implemented."
    ])

    leadership_insights.extend([
        "Effective ministry leadership combines spiritual discernment with responsible stewardship."
    ])

    return {
        "decision_explanations": decision_explanations,
        "strategic_guidance": strategic_guidance,
        "recommended_actions": recommended_actions,
        "scenario_answers": scenario_answers,
        "leadership_insights": leadership_insights
    }


def format_ministry_decision_response(question):

    guidance = generate_ministry_decision_guidance(question)

    response = []

    response.append("🧠 Ministry Decision Intelligence\n")

    for key, items in guidance.items():
        response.append(key.replace("_", " ").title())

        for item in items:
            response.append(f"- {item}")

        response.append("")

    return "\n".join(response)
