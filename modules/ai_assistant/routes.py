from flask import Blueprint, render_template, request, make_response, abort
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask_login import login_required, current_user
from models import ChurchEvent, db, BibleQuiz, Member, AcademicWork, AcademicDocument, AIConversation, MinistryProfile, ChurchProfile, PastorProfile, MinistryOccasion, MinistryContent, ActivityLog
from datetime import datetime
import requests
import os
from modules.content_generator.data import CONTENT_TYPES
from .intent_engine import detect_module
from .analytics import get_ai_statistics
from .dashboard import get_ai_dashboard
from .pdf_export import create_pdf
from .reports import generate_ai_report
from .insights import generate_ministry_insights
from .ministry_decision_engine import format_ministry_decision_response
from .ministry_copilot import format_ministry_copilot_response
from modules.ai_service import ask_ai, AI_LAST_STATUS, AI_LAST_STATUS
from modules.content_generator.flyer_composer_v5 import ai_compose_flyer
from modules.ministry_intelligence.occasion import build_occasion_context
from modules.content_generator.fal_service import generate_birthday_background
from .memory_engine import save_ministry_memory


ai_assistant_bp = Blueprint(
    "ai_assistant",
    __name__,
    url_prefix="/ai"
)


def save_ministry_content(
    occasion,
    content_type,
    title,
    content,
    ai_action=None,
    parent_id=None
):
    saved_content = MinistryContent(
        owner_id=occasion.created_by,
        occasion_id=occasion.id,
        content_type=content_type,
        title=title,
        content=content,
        version_number=1,
        parent_id=parent_id,
        ai_action=ai_action
    )

    db.session.add(saved_content)
    db.session.commit()

    return saved_content


def log_ministry_activity(
    action,
    module,
    details=None
):
    activity = ActivityLog(
        user_id=current_user.id if current_user.is_authenticated else None,
        action=action,
        module=module,
        details=details
    )

    db.session.add(activity)
    db.session.commit()

    return activity


def save_member_ai_content(
    member,
    content_type,
    title,
    content,
    ai_action=None
):
    saved_content = MinistryContent(
        owner_id=member.owner_id,
        occasion_id=None,
        content_type=content_type,
        title=title,
        content=content,
        version_number=1,
        ai_action=ai_action
    )

    db.session.add(saved_content)
    db.session.commit()

    return saved_content




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






def generate_content_plan(topic, audience, content_type):
    topic = topic or "Christian Growth"
    audience = audience or "Church Members"
    content_type = content_type or "Bible Study"

    return {
        "title": f"{topic}: A {content_type} Guide",
        "theme": f"Growing in Christ through {topic}",
        "scriptures": [
            "John 15:5",
            "2 Timothy 3:16",
            "Romans 12:2"
        ],
        "outline": [
            f"Introduction to {topic}",
            f"Biblical understanding of {topic}",
            f"Practical application for {audience}",
            "Prayer and reflection"
        ],
        "audience": audience,
        "content_type": content_type
    }


def generate_content_creator(plan):
    """Generate a complete ministry content draft from a content plan."""

    title = plan.get("title", "")
    theme = plan.get("theme", "")
    audience = plan.get("audience", "")
    scriptures = plan.get("scriptures", [])
    outline = plan.get("outline", [])

    content = f"""# {title}

Theme:
{theme}

Target Audience:
{audience}

Key Scriptures:
"""
    for verse in scriptures:
        content += f"- {verse}\n"

    content += "\nOutline:\n"
    for item in outline:
        content += f"- {item}\n"

    content += """

Teaching Notes:
Expand each outline point with biblical explanation, practical application, and relevant illustrations.

Prayer:
Close with a prayer asking God to help participants apply these truths in daily life.
"""

    return content


def generate_content_publisher(draft, format_type):
    """Transform ministry content into publishing formats."""

    draft = draft or ""
    format_type = format_type or "Website Article"

    if format_type == "Social Media Post":
        return f"""🙏 {draft}

Share this message and encourage others to grow in Christ.
#ChristianGrowth #Faith #Discipleship
"""

    elif format_type == "Flyer Content":
        return f"""TITLE:
{draft.splitlines()[0] if draft else "Christian Ministry Event"}

MESSAGE:
{draft}

Join us and be blessed.
"""

    elif format_type == "PDF Resource":
        return f"""MINISTRY RESOURCE

{draft}

Prepared for Christian teaching and discipleship.
"""

    else:
        return f"""ARTICLE TITLE

{draft}

This article provides biblical encouragement and practical application for believers.
"""


def prepare_flyer_content(title, content):
    """Prepare ministry content for Flyer Composer."""

    title = title or "Christian Ministry Event"
    content = content or ""

    return {
        "title": title,
        "headline": title,
        "message": content,
        "call_to_action": "Join us and be blessed.",
        "theme": "Growing in Christ"
    }


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




def save_ai_conversation(user_id, question, module, response):

    conversation = AIConversation(
        user_id=user_id,
        question=question,
        module=module or "general",
        response=response
    )

    db.session.add(conversation)
    db.session.commit()

    return conversation




def birthday_greeting_fallback(member):
    return f"""
🎉 Happy Birthday, {member.full_name}!

We thank God for His faithfulness, love, and mercy upon your life.
May this new year bring you deeper fellowship with God, renewed strength,
divine wisdom, and abundant blessings.

"The LORD bless thee, and keep thee:
The LORD make his face shine upon thee, and be gracious unto thee:
The LORD lift up his countenance upon thee, and give thee peace."
— Numbers 6:24-26

May God's purpose for your life continue to be fulfilled in Jesus' name.

Happy Birthday and many more fruitful years!
"""


def birthday_prayer_fallback(member):
    return f"""
🙏 Birthday Prayer for {member.full_name}

Heavenly Father, we thank You for the life of Your servant,
{member.full_name}.

Thank You for Your protection, guidance, and faithfulness.
As {member.full_name} begins another year, grant wisdom, good health,
spiritual growth, and success according to Your will.

May Your presence go before, Your grace sustain, and Your blessings
overflow in every area of life.

"For He shall give His angels charge over thee, to keep thee in all thy ways."
— Psalm 91:11

In Jesus' name, Amen.
"""


def ask_ai_with_memory(question, module=None):

    prompt = build_personalized_prompt(
        question,
        module
    )

    return ask_ai(prompt)






@ai_assistant_bp.route("/reports/pdf")
@login_required
def reports_pdf():

    report = generate_ai_report(
        current_user.id,
        "week"
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "InChristAlone AI Ministry Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"Period: {report['period']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Total AI Requests: {report['total_requests']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Most Used Module: {report['top_module']}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Module Usage:",
            styles["Heading2"]
        )
    )

    for module, count in report["modules"].items():

        elements.append(
            Paragraph(
                f"{module}: {count}",
                styles["Normal"]
            )
        )


    doc.build(elements)

    buffer.seek(0)

    response = make_response(
        buffer.read()
    )

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = (
        "attachment; filename=AI_Ministry_Report.pdf"
    )

    return response



@ai_assistant_bp.route("/insights")
@login_required
def insights():

    insight = generate_ministry_insights(
        current_user.id
    )

    return render_template(
        "ai_assistant/insights.html",
        insight=insight
    )


@ai_assistant_bp.route("/reports")
@login_required
def reports():

    report = generate_ai_report(
        current_user.id,
        "week"
    )

    return render_template(
        "ai_assistant/reports.html",
        report=report
    )



@ai_assistant_bp.route("/dashboard")
@login_required
def dashboard():

    data = get_ai_dashboard(
        current_user.id
    )

    return render_template(
        "ai_assistant/dashboard.html",
        data=data
    )


@ai_assistant_bp.route("/analytics")
@login_required
def analytics():

    stats = get_ai_statistics(
        current_user.id
    )

    return render_template(
        "ai_assistant/analytics.html",
        stats=stats
    )




@ai_assistant_bp.route("/export-report")
@login_required
def export_report():

    import csv
    from io import StringIO
    from flask import Response

    conversations = AIConversation.query.filter_by(
        user_id=current_user.id
    ).all()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Date",
        "Module",
        "Question",
        "Response"
    ])

    for item in conversations:
        writer.writerow([
            item.created_at,
            item.module,
            item.question,
            item.response
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=ai_ministry_report.csv"
        }
    )


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



@ai_assistant_bp.route("/content-planner", methods=["GET", "POST"])
@login_required
def content_planner():

    plan = None
    saved_message = None

    if request.method == "POST":

        action = request.form.get("action")

        if action == "save":
            title = request.form.get("title")
            content = request.form.get("content")
            content_type = request.form.get("content_type")

            saved = MinistryContent(
                owner_id=current_user.id,
                content_type=content_type,
                title=title,
                content=content,
                version_number=1,
                ai_action="content_planner"
            )

            db.session.add(saved)
            db.session.commit()

            saved_message = "✅ Content plan saved to Ministry Library."

        else:
            topic = request.form.get("topic")
            audience = request.form.get("audience")
            content_type = request.form.get("content_type")

            plan = generate_content_plan(
                topic,
                audience,
                content_type
            )

    return render_template(
        "ai_assistant/content_planner.html",
        plan=plan,
        saved_message=saved_message
    )



@ai_assistant_bp.route("/content-creator", methods=["GET", "POST"])
@login_required
def content_creator():

    plan = None
    draft = None
    saved_message = None

    if request.method == "POST":

        action = request.form.get("action")

        if action == "save":

            title = request.form.get("title")
            content = request.form.get("content")
            content_type = request.form.get("content_type")

            saved = MinistryContent(
                owner_id=current_user.id,
                content_type=content_type,
                title=title,
                content=content,
                version_number=1,
                ai_action="content_creator"
            )

            db.session.add(saved)
            db.session.commit()

            saved_message = "✅ Created content saved to Ministry Library."

        else:

            topic = request.form.get("topic")
            audience = request.form.get("audience")
            content_type = request.form.get("content_type")

            plan = generate_content_plan(
                topic,
                audience,
                content_type
            )

            draft = generate_content_creator(plan)

    return render_template(
        "ai_assistant/content_creator.html",
        plan=plan,
        draft=draft,
        saved_message=saved_message
    )


@ai_assistant_bp.route("/content-publisher", methods=["GET", "POST"])
@login_required
def content_publisher():

    published = None

    if request.method == "POST":

        draft = request.form.get("draft")
        format_type = request.form.get("format_type")

        published = generate_content_publisher(
            draft,
            format_type
        )

    return render_template(
        "ai_assistant/content_publisher.html",
        published=published
    )


@ai_assistant_bp.route("/content-flyer", methods=["GET", "POST"])
@login_required
def content_flyer():
    flyer_result = None
    draft = None

    if request.method == "POST":
        topic = request.form.get("topic")
        audience = request.form.get("audience")
        content_type = request.form.get("content_type")

        plan = generate_content_plan(
            topic,
            audience,
            content_type
        )

        draft = generate_content_creator(plan)

        flyer_content = prepare_flyer_content(
            topic,
            draft
        )

        flyer_result = ai_compose_flyer(
            title=topic,
            bible_verse="",
            theme="default",
            church_id=current_user.id
        )


    return render_template(
        "ai_assistant/content_flyer.html",
        flyer_result=flyer_result,
        draft=draft
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

        elif module == "ministry_intelligence":
            title = "🧠 AI Ministry Copilot"
            response = format_ministry_copilot_response()

        else:
            title = "🤖 AI Assistant"
            response = ask_ai_with_memory(question, module)



        answer = f"""
{title}

{response}

Your request:
{question}
"""



        save_ai_conversation(
            current_user.id,
            question,
            module,
            response
        )

    return render_template(
        "ai_assistant/chat.html",
        answer=answer
    )


@ai_assistant_bp.route("/birthday-greeting/<int:member_id>")
@login_required
def birthday_greeting(member_id):

    member = Member.query.get_or_404(member_id)

    if not member:
        return "Member not found", 404

    prompt = f"""
Create a warm Christian birthday greeting.

Member name: {member.full_name}

Include:
- appreciation for God's faithfulness
- a Bible verse
- prayerful blessings
- encouraging words for the new year of life

Write it as a message that can be sent by a pastor or church family.
"""

    response = ask_ai_with_memory(
        prompt,
        "birthday"
    )

    if response.startswith("⚠️"):
        response = (
            "ℹ️ AI assistant temporarily unavailable. "
            "A prepared ministry greeting has been provided.\n\n"
            + birthday_greeting_fallback(member)
        )

    save_member_ai_content(
        member,
        "Birthday Greeting",
        f"Birthday Greeting - {member.full_name}",
        response,
        ai_action="Member Birthday Greeting"
    )

    log_ministry_activity(
        "Birthday Greeting Generated",
        "AI Assistant",
        f"Generated birthday greeting for {member.full_name}"
    )

    save_ministry_memory(
        title=f"Birthday Care Engagement - {member.full_name}",
        content=f"AI generated a birthday greeting for {member.full_name}. This indicates an opportunity for personalized member care and relationship building.",
        memory_type="Member Engagement",
        source="AI Birthday Assistant",
        importance="Medium",
        user_id=current_user.id
    )

    return render_template(
        "church_management/member_ai_result.html",
        member=member,
        title="🎂 Birthday Greeting",
        content=response,
        flyer=None
    )


@ai_assistant_bp.route("/birthday-prayer/<int:member_id>")
@login_required
def birthday_prayer(member_id):

    member = Member.query.get_or_404(member_id)

    if not member:
        return "Member not found", 404

    prompt = f"""
Write a Christian birthday prayer for {member.full_name}.

Include:
- thanksgiving to God
- prayers for spiritual growth
- divine guidance
- God's protection and purpose
- relevant Scripture references
"""

    response = ask_ai_with_memory(
        prompt,
        "birthday"
    )

    if response.startswith("⚠️"):
        response = birthday_prayer_fallback(member)

    save_member_ai_content(
        member,
        "Birthday Prayer",
        f"Birthday Prayer - {member.full_name}",
        response,
        ai_action="Member Birthday Prayer"
    )

    log_ministry_activity(
        "Birthday Prayer Generated",
        "AI Assistant",
        f"Generated birthday prayer for {member.full_name}"
    )

    save_ministry_memory(
        title=f"Birthday Prayer Engagement - {member.full_name}",
        content=f"AI generated a birthday prayer for {member.full_name}. This supports personalized spiritual care and member connection.",
        memory_type="Member Engagement",
        source="AI Birthday Assistant",
        importance="Medium",
        user_id=current_user.id
    )

    return render_template(
        "church_management/member_ai_result.html",
        member=member,
        title="🙏 Birthday Prayer",
        content=response,
        flyer=None
    )





@ai_assistant_bp.route("/occasion-prayer/<int:occasion_id>")
@login_required
def occasion_prayer(occasion_id):

    occasion = MinistryOccasion.query.get_or_404(
        occasion_id
    )

    prompt = f"""
Write a Christian prayer for this ministry occasion.

Occasion:
{occasion.title}

Type:
{occasion.occasion_type}

Theme:
{occasion.description}

Scripture theme:
{occasion.scripture_theme}

Include:
- thanksgiving to God
- spiritual impact
- prayers for participants
- relevant Bible references
"""

    response = ask_ai_with_memory(
        prompt,
        "occasion"
    )

    save_ministry_content(
        occasion,
        "Prayer",
        f"Prayer - {occasion.title}",
        response,
        ai_action="Occasion Prayer"
    )

    return render_template(
        "church_management/member_ai_result.html",
        title="🙏 Occasion Prayer",
        content=response,
        flyer=None
    )


@ai_assistant_bp.route("/occasion-announcement/<int:occasion_id>")
@login_required
def occasion_announcement(occasion_id):

    occasion = MinistryOccasion.query.get_or_404(
        occasion_id
    )

    prompt = f"""
Create a Christian ministry announcement.

Occasion:
{occasion.title}

Type:
{occasion.occasion_type}

Description:
{occasion.description}

Date:
{occasion.date}

Make it suitable for church members.
Include invitation and encouragement.
"""

    response = ask_ai_with_memory(
        prompt,
        "occasion"
    )

    save_ministry_content(
        occasion,
        "Announcement",
        f"Announcement - {occasion.title}",
        response,
        ai_action="Occasion Announcement"
    )

    return render_template(
        "church_management/member_ai_result.html",
        title="📢 Occasion Announcement",
        content=response,
        flyer=None
    )


@ai_assistant_bp.route("/occasion-outline/<int:occasion_id>")
@login_required
def occasion_outline(occasion_id):

    occasion = MinistryOccasion.query.get_or_404(
        occasion_id
    )

    prompt = f"""
Create a Bible study outline for this ministry occasion.

Title:
{occasion.title}

Theme:
{occasion.description}

Scripture:
{occasion.scripture_theme}

Provide:
- Introduction
- Bible passages
- Teaching points
- Discussion questions
- Application
"""

    response = ask_ai_with_memory(
        prompt,
        "occasion"
    )

    save_ministry_content(
        occasion,
        "Bible Study Outline",
        f"Study Outline - {occasion.title}",
        response,
        ai_action="Occasion Bible Study Outline"
    )

    return render_template(
        "church_management/member_ai_result.html",
        title="📖 Occasion Bible Study Outline",
        content=response,
        flyer=None
    )


def download_fal_background(image_url):
    try:
        response = requests.get(
            image_url,
            timeout=30
        )

        if response.status_code == 200:
            os.makedirs(
                "static/generated",
                exist_ok=True
            )

            path = "static/generated/birthday_ai_background.jpg"

            with open(path, "wb") as f:
                f.write(response.content)

            return path

    except Exception:
        pass

    return None



@ai_assistant_bp.route("/event-flyer/<int:event_id>")
@login_required
def event_flyer(event_id):

    event = ChurchEvent.query.get_or_404(event_id)

    church = ChurchProfile.query.get(event.church_id) if event.church_id else None

    pastor = PastorProfile.query.get(event.pastor_id) if event.pastor_id else None

    ai_event_content = generate_content_creator(
        generate_content_plan(
            event.title,
            "Church Members",
            "Event Flyer"
        )
    )

    speakers = []

    if pastor:
        speakers.append({
            "photo": pastor.photo_filename,
            "name": pastor.full_name,
            "role": "Host Pastor"
        })

    flyer_result = ai_compose_flyer(
        title=event.title,
        bible_verse="",
        event_date=str(event.start_datetime),
        venue=event.venue or event.location or "",
        speakers=speakers or None,
        logo_path=church.logo_filename if church else None,
        theme="default"
    )

    return render_template(
        "church_management/member_ai_result.html",
        title="🎨 Programme Flyer",
        content=ai_event_content,
        flyer=flyer_result.get("file")
    )




@ai_assistant_bp.route("/occasion-flyer/<int:occasion_id>")
@login_required
def occasion_flyer(occasion_id):

    occasion = MinistryOccasion.query.get_or_404(
        occasion_id
    )

    context = build_occasion_context(
        occasion
    )

    church = (
        ChurchProfile.query.get(occasion.church_id)
        if occasion.church_id
        else None
    )

    speakers = []

    flyer_result = ai_compose_flyer(
        title=context["title"],
        bible_verse=context.get("scripture_theme") or "",
        event_date=str(context["date"]),
        venue=context.get("description") or "",
        speakers=speakers or None,
        logo_path=(
            church.logo_filename
            if church
            else None
        ),
        theme="default"
    )

    save_ministry_content(
        occasion,
        "Flyer",
        f"Flyer - {occasion.title}",
        str(flyer_result),
        ai_action="Occasion Flyer"
    )

    return render_template(
        "church_management/member_ai_result.html",
        title="🎨 Occasion Flyer",
        content=context["description"] or context["title"],
        flyer=flyer_result.get("file")
    )


@ai_assistant_bp.route("/birthday-flyer/<int:member_id>")
@login_required
def birthday_flyer(member_id):

    member = Member.query.get_or_404(member_id)

    church = ChurchProfile.query.filter_by(
        owner_id=member.owner_id
    ).first()

    pastor = PastorProfile.query.filter_by(
        church_id=church.id
    ).first() if church else None

    background_url = generate_birthday_background(
        member.full_name
    )

    background_path = download_fal_background(
        background_url
    )

    flyer_result = ai_compose_flyer(
        title=f"Happy Birthday {member.full_name}",
        bible_verse="Numbers 6:24-26",
        event_date=str(member.birthday),
        venue=(
            f"Celebrating God's faithfulness\n{church.church_name}"
            if church
            else "Celebrating God's faithfulness"
        ),
        speakers=(
            [
                {
                    "photo": member.profile_photo,
                    "name": member.full_name,
                    "role": "Birthday Celebration"
                }
            ]
            +
            [
                {
                    "photo": pastor.photo_filename,
                    "name": pastor.full_name,
                    "role": "Senior Pastor"
                }
            ]
            if pastor and pastor.photo_filename
            else []
        )
        if member.profile_photo else None,
        logo_path=church.logo_filename if church else None,
          background_path=background_path,
        theme="default"
    )

    generated_image = flyer_result.get("file")

    log_ministry_activity(
        "Birthday Flyer Created",
        "AI Assistant",
        f"Created birthday flyer for {member.full_name}"
    )

    save_ministry_memory(
        title=f"Birthday Flyer Engagement - {member.full_name}",
        content=f"AI generated a birthday flyer for {member.full_name}. This supports personalized celebration and member connection.",
        memory_type="Member Engagement",
        source="AI Birthday Assistant",
        importance="Medium",
        user_id=current_user.id
    )

    return render_template(
        "church_management/member_ai_result.html",
        member=member,
        title="🎨 Birthday Flyer Created",
        content=f"Birthday flyer generated for {member.full_name}",
        flyer=generated_image
    )


@ai_assistant_bp.route("/content-similar/<int:content_id>")
@login_required
def content_similar(content_id):

    saved = MinistryContent.query.get_or_404(content_id)

    if saved.owner_id != current_user.id:
        abort(403)

    prompt = f"""
Rewrite the following Christian ministry content.

Keep the same biblical message and purpose,
but create a fresh original version.

Title:
{saved.title}

Content Type:
{saved.content_type}

Content:
{saved.content}
"""

    response = ask_ai_with_memory(
        prompt,
        "content_library"
    )

    latest_version = db.session.query(
        db.func.max(MinistryContent.version_number)
    ).filter(
        MinistryContent.parent_id == saved.id
    ).scalar()

    next_version = (latest_version or saved.version_number or 1) + 1

    version = MinistryContent(
        owner_id=saved.owner_id,
        occasion_id=saved.occasion_id,
        content_type=saved.content_type,
        title=saved.title,
        content=response,
        version_number=next_version,
        parent_id=saved.id,
        ai_action="Generate Similar"
    )

    db.session.add(version)
    db.session.commit()

    return render_template(
        "church_management/member_ai_result.html",
        title="🔄 Similar Ministry Content",
        content=response,
        flyer=None
    )
