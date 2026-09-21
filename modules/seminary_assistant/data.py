TOPIC_REFINEMENT_PROMPTS = {
    "narrow_topic": {
        "label": "Narrow a Broad Topic",
        "fields": ["broad_topic", "field_of_study", "constraints"],
        "template": (
            "Act as a doctoral research advisor in theology and church leadership.\n\n"
            "I have a broad topic idea: \"{broad_topic}\".\n"
            "Field of study: {field_of_study}.\n"
            "Constraints (time, access to data, scope): {constraints}.\n\n"
            "Help me narrow this into 3-5 specific, researchable topic options, "
            "each with a working title, why it's researchable, and a possible research question."
        ),
    },
    "research_question": {
        "label": "Develop Research Questions",
        "fields": ["topic", "research_gap"],
        "template": (
            "Act as a dissertation committee chair.\n\n"
            "Topic: \"{topic}\".\n"
            "Identified research gap: {research_gap}.\n\n"
            "Generate 3 well-formed research questions (one primary, two secondary) "
            "that are specific, researchable, and aligned with the identified gap."
        ),
    },
    "title_refinement": {
        "label": "Refine Thesis Title",
        "fields": ["draft_title", "key_variables"],
        "template": (
            "Act as an academic editor specializing in dissertation titles.\n\n"
            "Draft title: \"{draft_title}\".\n"
            "Key variables/concepts to reflect: {key_variables}.\n\n"
            "Suggest 3 refined title options that are concise, clearly indicate the study's "
            "variables and context, and follow standard dissertation title conventions."
        ),
    },
    "seminar_topic": {
        "label": "Seminar Paper Topic Idea",
        "fields": ["course_subject", "interest_area", "length_requirement"],
        "template": (
            "Act as a seminary professor helping a student choose a seminar paper topic.\n\n"
            "Course subject: {course_subject}.\n"
            "Area of interest: {interest_area}.\n"
            "Length requirement: {length_requirement}.\n\n"
            "Suggest 3 seminar paper topics that fit the course, are appropriately scoped "
            "for the length requirement, and allow for solid theological/academic engagement."
        ),
    },
}


WORK_TYPES = {
    "thesis_chapter": "Thesis Chapter",
    "seminar_paper": "Seminar Paper",
    "assignment": "Assignment",
}

WORK_STATUSES = {
    "not_started": "Not Started",
    "in_progress": "In Progress",
    "submitted": "Submitted",
    "approved": "Approved",
}