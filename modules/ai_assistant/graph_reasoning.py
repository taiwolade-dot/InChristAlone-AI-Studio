from collections import Counter


MINISTRY_THEMES = {
    "discipleship": [
        "discipleship",
        "disciple",
        "spiritual growth"
    ],
    "leadership": [
        "leadership",
        "leader",
        "servant"
    ],
    "growth": [
        "growth",
        "development",
        "increase",
        "improvement"
    ],
    "strategy": [
        "strategy",
        "planning",
        "recommendation"
    ],
    "training": [
        "training",
        "learning",
        "development"
    ]
}


def extract_memory_text(graph):

    texts = []

    for item in graph:

        texts.append(
            item.get("source", "")
        )

        texts.append(
            item.get("target", "")
        )

    return " ".join(texts).lower()



def detect_ministry_themes(graph):

    text = extract_memory_text(graph)

    detected = Counter()

    for theme, keywords in MINISTRY_THEMES.items():

        for keyword in keywords:

            if keyword in text:
                detected[theme] += 1


    return dict(detected)



def generate_graph_reasoning(graph):

    themes = detect_ministry_themes(graph)

    strength = "Low"

    if len(themes) >= 3:
        strength = "High"

    elif len(themes) == 2:
        strength = "Medium"


    return {
        "dominant_themes": themes,
        "connection_strength": strength,
        "relationship_count": len(graph)
    }


def generate_ministry_insight(reasoning):

    themes = reasoning.get(
        "dominant_themes",
        {}
    )

    strength = reasoning.get(
        "connection_strength",
        "Low"
    )


    if not themes:
        return (
            "No significant ministry patterns "
            "have been identified yet."
        )


    primary = max(
        themes,
        key=themes.get
    )


    return (
        "The knowledge graph indicates a recurring "
        f"emphasis on {primary}. "
        f"Connection strength is {strength}. "
        "Future ministry strategies should consider "
        f"strengthening {primary} initiatives."
    )
