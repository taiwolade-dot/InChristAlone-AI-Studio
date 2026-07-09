PROMPT_CATEGORIES = {
    "sermon_prep": {
        "label": "Sermon Preparation",
        "fields": ["topic", "scripture", "audience", "tone"],
        "template": (
            "Act as an experienced Christian pastor and homiletics expert.\n\n"
            "Prepare a sermon outline on the topic: \"{topic}\".\n"
            "Primary scripture reference: {scripture}.\n"
            "Audience: {audience}.\n"
            "Tone: {tone}.\n\n"
            "Include: an engaging introduction, 3 clear points with supporting scripture, "
            "practical application for daily life, and a closing call to action."
        ),
    },
    "bible_study": {
        "label": "Bible Study Guide",
        "fields": ["passage", "audience", "duration"],
        "template": (
            "Act as a Bible study facilitator preparing material for {audience}.\n\n"
            "Create a Bible study guide on the passage: {passage}.\n"
            "Session duration: {duration}.\n\n"
            "Include: context/background, key verses to discuss, 5 discussion questions, "
            "and a closing prayer prompt."
        ),
    },
    "counseling": {
        "label": "Pastoral Counseling Support",
        "fields": ["situation", "scripture_focus"],
        "template": (
            "Act as a wise, compassionate Christian counselor.\n\n"
            "A church member is dealing with: {situation}.\n"
            "Provide biblically grounded guidance, referencing {scripture_focus} where relevant, "
            "along with 3 practical steps and a prayer they can pray."
        ),
    },
    "youth_ministry": {
        "label": "Youth Ministry Content",
        "fields": ["topic", "age_group", "format"],
        "template": (
            "Act as a creative youth pastor.\n\n"
            "Create content on the topic \"{topic}\" for {age_group}.\n"
            "Format: {format}.\n\n"
            "Make it engaging, relatable to modern youth culture, and rooted in scripture."
        ),
    },
    "content_creation": {
        "label": "Christian Social Media Content",
        "fields": ["platform", "theme", "cta"],
        "template": (
            "Act as a Christian content strategist.\n\n"
            "Write a {platform} post on the theme: \"{theme}\".\n"
            "End with this call to action: {cta}.\n\n"
            "Keep it concise, scripture-anchored, and shareable."
        ),
    },
}