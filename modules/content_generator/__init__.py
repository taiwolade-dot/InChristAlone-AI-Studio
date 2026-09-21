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
        "fields": ["event_title", "date_time", "location", "key_message", "color_preference"],
        "template": (
            "Design a promotional flyer.\n\n"
            "Event Title: {event_title}.\n"
            "Date & Time: {date_time}.\n"
            "Location: {location}.\n"
            "Key Message: {key_message}.\n"
            "Color Preference: {color_preference}.\n\n"
            "Layout: bold title at top, clear date/time/location block, "
            "supporting scripture or tagline, clean modern church-flyer design, "
            "royal blue and gold accents unless otherwise specified."
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
}