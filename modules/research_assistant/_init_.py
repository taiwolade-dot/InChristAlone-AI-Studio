RESEARCH_PROMPTS = {
    "literature_review": {
        "label": "Literature Review Section",
        "fields": ["topic", "key_themes", "scope"],
        "template": (
            "Act as a doctoral research assistant specializing in theology and church leadership studies.\n\n"
            "Write a literature review section on: \"{topic}\".\n"
            "Key themes to cover: {key_themes}.\n"
            "Scope: {scope}.\n\n"
            "Structure it with: an introduction to the body of literature, thematic organization "
            "(not just source-by-source), identification of gaps in existing research, "
            "and a transition into the study's contribution."
        ),
    },
    "methodology": {
        "label": "Methodology Chapter Support",
        "fields": ["research_design", "population", "data_collection"],
        "template": (
            "Act as a doctoral research methodology advisor.\n\n"
            "Help draft a methodology section using a {research_design} approach.\n"
            "Study population: {population}.\n"
            "Data collection method: {data_collection}.\n\n"
            "Include: rationale for the chosen design, population/sampling justification, "
            "data collection procedure, and validity/reliability considerations."
        ),
    },
    "thesis_intro": {
        "label": "Thesis Introduction / Problem Statement",
        "fields": ["research_topic", "problem_statement", "significance"],
        "template": (
            "Act as an academic writing advisor for a doctoral thesis in servant leadership and church vitality.\n\n"
            "Topic: \"{research_topic}\".\n"
            "Problem statement: {problem_statement}.\n"
            "Significance of the study: {significance}.\n\n"
            "Draft an introduction chapter opening that establishes context, states the problem clearly, "
            "and justifies the study's significance to Nigerian Baptist church leadership."
        ),
    },
    "discussion_chapter": {
        "label": "Discussion / Findings Interpretation",
        "fields": ["key_findings", "theoretical_framework"],
        "template": (
            "Act as a doctoral dissertation committee advisor.\n\n"
            "Help interpret these key findings: {key_findings}.\n"
            "Theoretical framework: {theoretical_framework}.\n\n"
            "Structure the discussion to: relate findings back to the literature, "
            "explain implications for practice (pastoral ministry), and note limitations."
        ),
    },
}


CITATION_STYLES = {
    "apa7": {
        "label": "APA 7th Edition",
    },
    "turabian": {
        "label": "Turabian/Chicago (NBTS Ogbomoso Style)",
    },
}