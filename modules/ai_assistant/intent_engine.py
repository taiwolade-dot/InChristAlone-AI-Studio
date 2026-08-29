def detect_module(question):

    q = question.lower()


    if any(word in q for word in [
        "programme",
        "program",
        "event",
        "calendar",
        "conference",
        "association",
        "convention",
        "meeting",
        "schedule"
    ]):
        return "calendar"


    if any(word in q for word in [
        "quiz",
        "bible quiz",
        "question",
        "competition",
        "answer"
    ]):
        return "quiz"


    if any(word in q for word in [
        "member",
        "membership",
        "birthday",
        "baptism",
        "church member",
        "pastor",
        "leader"
    ]):
        return "members"


    if any(word in q for word in [
        "sermon",
        "preaching",
        "message",
        "outline",
        "homily"
    ]):
        return "sermon"


    if any(word in q for word in [
        "prayer",
        "prayers",
        "fasting",
        "intercession",
        "devotion"
    ]):
        return "prayer"


    if any(word in q for word in [
        "worship",
        "song",
        "hymn",
        "praise"
    ]):
        return "worship"


    if any(word in q for word in [
        "research",
        "thesis",
        "seminary",
        "academic",
        "paper"
    ]):
        return "seminary"


    if any(word in q for word in [
        "flyer",
        "poster",
        "graphic",
        "video",
        "content"
    ]):
        return "content"


    if any(word in q for word in [
        "help",
        "how do i",
        "how can i",
        "what can you do"
    ]):
        return "ai_help"


    return "general"
