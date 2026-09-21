CONTENT_TYPES = {
    "cartoon": {
        "label": "Cartoon / Animation",
        "fields": ["character_description", "scene_setting", "action", "mood", "art_style"],
        "template": (
            "Create a cartoon/animation-style image.\n\n"
            "Character: {character_description}.\n"
            "Scene/Setting: {scene_setting}.\n"
            "Action: {action}.\n"
            "Mood: {mood}.\n"
            "Art Style: {art_style}.\n\n"
            "Rendered in a warm, family-friendly Christian animation style, "
            "vivid colors, clean linework, expressive character emotion."
        ),
    },
    "flyer": {
        "label": "Flyer / Graphic Design",
        "fields": [
            "title",
            "bible_verse",
            "event_date",
            "venue",
            "theme",
            "design_style",
            "color_preference",
            "mood"
        ],
        "template": (
            "Create a premium Christian flyer design.\n\n"
            "Title: {title}.\n"
            "Bible Verse: {bible_verse}.\n"
            "Event Date: {event_date}.\n"
            "Venue: {venue}.\n"
            "Theme: {theme}.\n"
            "Design Style: {design_style}.\n"
            "Colours: {color_preference}.\n"
            "Mood: {mood}.\n\n"
            "Create a professional church flyer composition "
            "with elegant Christian atmosphere, balanced layout, "
            "high quality typography space, speaker photo areas, "
            "and premium ministry branding."
        ),
    },

    "video": {
        "label": "Video Script & Shot List",
        "fields": ["video_topic", "target_length", "audience", "call_to_action"],
        "template": (
            "Act as a Christian video content director.\n\n"
            "Write a video script and shot list on: \"{video_topic}\".\n"
            "Target length: {target_length}.\n"
            "Audience: {audience}.\n"
            "Call to action: {call_to_action}.\n\n"
            "Structure: Hook (first 5 seconds), main content broken into scenes with shot "
            "descriptions, on-screen text suggestions, and closing call to action."
        ),
    },
    "music": {
        "label": "Music / Song Concept",
        "fields": ["song_theme", "genre", "mood", "key_lyric_idea"],
        "template": (
            "Act as a Christian songwriter and music producer.\n\n"
            "Create a song concept on the theme: \"{song_theme}\".\n"
            "Genre: {genre}.\n"
            "Mood: {mood}.\n"
            "Key lyric idea to build around: {key_lyric_idea}.\n\n"
            "Provide: song title suggestion, verse/chorus structure outline, "
            "sample opening lines, and instrumentation/style notes."
        ),
    },
    "bible_study_outline": {
        "label": "Bible Study Outline",
        "fields": [
            "topic",
            "scripture",
            "audience",
            "theme",
            "key_points",
            "application"
        ],
        "template": (
            "Act as a Christian Bible Study teacher and curriculum developer.\n\n"
            "Create a Bible Study Outline on: {topic}.\n"
            "Primary Scripture: {scripture}.\n"
            "Audience: {audience}.\n"
            "Theme: {theme}.\n"
            "Key Points: {key_points}.\n"
            "Practical Application: {application}.\n\n"
            "Structure the outline with introduction, biblical background, "
            "major teaching points, discussion questions, practical applications, "
            "and prayer points."
        ),
    },
}
