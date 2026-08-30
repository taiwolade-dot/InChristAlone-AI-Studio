from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import ChurchEvent, db, BibleQuiz, Member, AcademicWork, AcademicDocument, AIConversation, MinistryProfile
from datetime import datetime
from modules.content_generator.data import CONTENT_TYPES
from .intent_engine import detect_module
from modules.ai_service import ask_ai


ai_assistant_bp = Blueprint(
    "ai_assistant",
    __name__,
    url_prefix="/ai"
)



def search_calendar(question):

    q = question.lower()

    query = ChurchEvent.query


    if "association" in q:
        query = query.filter(
            ChurchEvent.level == "Association"
        )

    elif "conference" in q:
        query = query.filter(
            ChurchEvent.level == "Conference"
        )

    elif "convention" in q:
        query = query.filter(
            ChurchEvent.level == "Convention"
        )


    if "youth" in q:
        query = query.filter(
            ChurchEvent.ministry == "Youth"
        )


    organization_map = {
        "nbc": "Nigerian Baptist Convention",
        "nba": "Nazareth Baptist Association",
        "fctbc": "FCT Baptist Conference",
        "fct baptist conference": "FCT Baptist Conference",
        "vbc": "Victory Baptist Church",
        "general": "General"
    }


    for keyword, org_name in organization_map.items():
        if keyword in q:
            query = query.filter(
                ChurchEvent.organization_name.ilike(
                    f"%{org_name}%"
                )
            )
            break


    for org in organization_map.values():
        if org in q:
            query = query.filter(
                ChurchEvent.organization_name.ilike(
                    f"%{org}%"
                )
            )
            break


    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }


    for month_name, month_number in months.items():
        if month_name in q:
            query = query.filter(
                db.extract(
                    "month",
                    ChurchEvent.start_datetime
                ) == month_number
            )
            break


    quarters = {
        "q1": (1, 3),
        "q2": (4, 6),
        "q3": (7, 9),
        "q4": (10, 12)
    }


    for quarter, (start_month, end_month) in quarters.items():
        if quarter in q:
            query = query.filter(
                db.extract(
                    "month",
                    ChurchEvent.start_datetime
                ).between(start_month, end_month)
            )
            break


    if "first half" in q or "h1" in q:
        query = query.filter(
            db.extract(
                "month",
                ChurchEvent.start_datetime
            ).between(1, 6)
        )


    if "second half" in q or "h2" in q:
        query = query.filter(
            db.extract(
                "month",
                ChurchEvent.start_datetime
            ).between(7, 12)
        )


    events = query.order_by(
        ChurchEvent.start_datetime.asc()
    ).limit(10).all()


    if not events:
        return "No matching programmes found."


    result = "📅 Programmes Found:\n\n"

    for event in events:
        result += (
            f"• {event.title}\n"
            f"  {event.organization_name}\n"
            f"  {event.start_datetime}\n"
            f"  {event.venue}\n\n"
        )

    return result






def generate_content(question):

    q = question.lower()


    if "flyer" in q or "poster" in q:
        content_type = "flyer"

    elif "video" in q or "script" in q:
        content_type = "video"

    elif "song" in q or "music" in q or "worship" in q:
        content_type = "music"

    else:
        content_type = "cartoon"


    template = CONTENT_TYPES.get(content_type)


    return (
        f"✍ Content Type: {template['label']}\n\n"
        "Your request has been identified for content generation.\n\n"
        f"Prompt Framework:\n{template['template']}"
    )


def search_seminary(question):

    q = question.lower()


    if "document" in q or "file" in q:

        documents = AcademicDocument.query.limit(10).all()

        if not documents:
            return "No academic documents found."


        result = "📄 Academic Documents:\n\n"

        for doc in documents:
            result += (
                f"• {doc.original_filename}\n"
            )

        return result


    works = AcademicWork.query.order_by(
        AcademicWork.created_at.desc()
    ).limit(10).all()


    if not works:
        return "No academic works found."


    result = "🎓 Academic Works:\n\n"

    for work in works:
        result += (
            f"• {work.title}\n"
            f"  Status: {work.status}\n"
            f"  Type: {work.work_type}\n\n"
        )

    return result


def search_members(question):

    q = question.lower()

    if "baptized" in q or "baptism" in q:
        count = Member.query.filter(
            Member.date_of_baptism.isnot(None)
        ).count()

        return (
            f"💧 Baptized Members: {count}"
        )


    # Name search
    words = q.split()

    ignored = [
        "find",
        "search",
        "show",
        "member",
        "members",
        "with",
        "name"
    ]

    search_terms = [
        word for word in words
        if word not in ignored
    ]


    if search_terms:

        for term in search_terms:

            members = Member.query.filter(
                Member.full_name.ilike(
                    f"%{term}%"
                )
            ).all()

            if members:

                result = "👥 Members Found:\n\n"

                for member in members:
                    result += (
                        f"• {member.full_name}\n"
                        f"  Role: {member.church_role}\n"
                        f"  Phone: {member.phone}\n\n"
                    )

                return result


    roles = [
        "pastor",
        "deacon",
        "leader",
        "worker"
    ]


    for role in roles:
        if role in q:

            members = Member.query.filter(
                Member.church_role.ilike(
                    f"%{role}%"
                )
            ).all()

            if not members:
                return f"No members found with role: {role}"


            result = f"👥 {role.title()}s Found:\n\n"

            for member in members:
                result += (
                    f"• {member.full_name}\n"
                    f"  Role: {member.church_role}\n\n"
                )

            return result


    if "how many" in q or "count" in q:
        count = Member.query.count()

        return (
            f"👥 Total Members: {count}"
        )


    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }


    for month_name, month_number in months.items():
        if month_name in q:
            members = Member.query.filter(
                db.extract(
                    "month",
                    Member.birthday
                ) == month_number
            ).all()

            if not members:
                return "No members found for that birthday month."

            result = "🎂 Birthday Members:\n\n"

            for member in members:
                result += (
                    f"• {member.full_name}\n"
                    f"  Birthday: {member.birthday}\n\n"
                )

            return result


    members = Member.query.order_by(
        Member.full_name.asc()
    ).limit(10).all()


    if not members:
        return "No members found."


    result = "👥 Members Found:\n\n"

    for member in members:
        result += (
            f"• {member.full_name}\n"
            f"  Role: {member.church_role}\n"
            f"  Phone: {member.phone}\n\n"
        )

    return result


def search_bible_quiz():

    quizzes = BibleQuiz.query.order_by(
        BibleQuiz.created_at.desc()
    ).limit(10).all()


    if not quizzes:
        return "No Bible quizzes found."


    result = "📖 Bible Quizzes:\n\n"

    for quiz in quizzes:
        result += (
            f"• {quiz.title}\n"
            f"  Age Group: {quiz.age_group}\n"
            f"  Questions: {len(quiz.questions)}\n\n"
        )

    return result


def get_ai_memory(user_id, limit=5):

    conversations = AIConversation.query.filter_by(
        user_id=user_id
    ).order_by(
        AIConversation.created_at.desc()
    ).limit(limit).all()

    if not conversations:
        return ""

    memory = "Previous conversation context:\n\n"

    for chat in reversed(conversations):
        memory += (
            f"User: {chat.question}\n"
            f"Assistant: {chat.response}\n\n"
        )

    return memory




def get_ministry_profile(user_id):

    profile = MinistryProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return ""

    return f"""
Ministry Profile

Church: {profile.church_name or ""}
Denomination: {profile.denomination or ""}
Role: {profile.ministry_role or ""}
Location: {profile.location or ""}
Preferred Sermon Style: {profile.preferred_sermon_style or ""}
Preferred Bible Translation: {profile.preferred_bible_translation or "KJV"}

"""




def build_personalized_prompt(question, module=None):

    profile = get_ministry_profile(current_user.id)
    memory = get_ai_memory(current_user.id)

    module_context = ""

    if module == "sermon":
        module_context = """
Prepare sermons with:
- Biblical exposition
- Clear sermon structure
- Introduction, points and conclusion
- Practical ministry application
"""

    elif module == "prayer":
        module_context = """
Prepare prayers with:
- Scripture foundation
- Pastoral tone
- Spiritual encouragement
- Faith declarations
"""

    elif module == "worship":
        module_context = """
Provide worship assistance with:
- Biblical themes
- Worship flow suggestions
- Appropriate spiritual emphasis
"""

    elif module == "research":
        module_context = """
Provide scholarly assistance with:
- Academic structure
- References
- Critical analysis
"""

    return f"""
{profile}

{memory}

{module_context}

User Request:
{question}
"""




def ask_ai_with_memory(question, module=None):

    prompt = build_personalized_prompt(
        question,
        module
    )

    return ask_ai(prompt)




@ai_assistant_bp.route("/history")
@login_required
def history():

    conversations = AIConversation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        AIConversation.created_at.desc()
    ).limit(50).all()

    return render_template(
        "ai_assistant/history.html",
        conversations=conversations
    )



@ai_assistant_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    profile = MinistryProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        if not profile:
            profile = MinistryProfile(
                user_id=current_user.id
            )

        profile.church_name = request.form.get("church_name")
        profile.denomination = request.form.get("denomination")
        profile.ministry_role = request.form.get("ministry_role")
        profile.location = request.form.get("location")
        profile.preferred_sermon_style = request.form.get("preferred_sermon_style")
        profile.preferred_bible_translation = request.form.get("preferred_bible_translation")

        db.session.add(profile)
        db.session.commit()

    return render_template(
        "ai_assistant/profile.html",
        profile=profile
    )



@ai_assistant_bp.route("/", methods=["GET", "POST"])
@login_required
def chat():

    answer = ""

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        )


        module = detect_module(
            question
        )


        if module == "quiz":
            title = "📖 Bible Quiz"
            response = search_bible_quiz()


        elif module == "calendar":
            title = "📅 Church Calendar"
            response = search_calendar(question)


        elif module == "members":
            title = "👥 Church Management"
            response = search_members(question)


        elif module == "seminary":
            title = "🎓 Seminary Assistant"
            response = search_seminary(question)


        elif module == "content":
            title = "✍ Content Generator"
            response = generate_content(question)


        elif module == "sermon":
            title = "🎤 Sermon Assistant"
            response = ask_ai_with_memory(question, module)

        elif module == "prayer":
            title = "🙏 Prayer Assistant"
            response = ask_ai_with_memory(question, module)

        elif module == "worship":
            title = "🎶 Worship Assistant"
            response = ask_ai_with_memory(question, module)

        elif module == "ai_help":
            title = "🤖 AI Studio Help"
            response = ask_ai_with_memory(question, module)

        else:
            title = "🤖 AI Assistant"
            response = ask_ai_with_memory(question, module)



        answer = f"""
{title}

{response}

Your request:
{question}
"""



        conversation = AIConversation(
            user_id=current_user.id,
            question=question,
            module=module,
            response=response
        )

        db.session.add(conversation)
        db.session.commit()

    return render_template(
        "ai_assistant/chat.html",
        answer=answer
    )
