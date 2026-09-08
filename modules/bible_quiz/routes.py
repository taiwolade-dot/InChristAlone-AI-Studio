from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from models import db, BibleQuiz, QuizQuestion, QuizLiveSession, QuizParticipant, QuizAnswer
from . import ai_generator

bible_quiz_bp = Blueprint(
    'bible_quiz',
    __name__,
    url_prefix='/bible-quiz',
    template_folder='../../templates/bible_quiz'
)


@bible_quiz_bp.route('/', methods=['GET'])
@login_required
def dashboard():

    ministry = getattr(current_user, "ministry_profile", None)

    if ministry:
        quizzes = BibleQuiz.query.filter_by(
            ministry_id=ministry.id
        ).order_by(
            BibleQuiz.created_at.desc()
        ).all()
    else:
        quizzes = BibleQuiz.query.filter_by(
            owner_id=current_user.id
        ).order_by(
            BibleQuiz.created_at.desc()
        ).all()

    return render_template(
        'bible_quiz/dashboard.html',
        quizzes=quizzes,
        ministry=ministry
    )


@bible_quiz_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_quiz():
    from modules.wallet_utils import spend_units, refund_units

    if request.method == 'POST':
        title = request.form['title'].strip()
        age_group = request.form['age_group']
        target_group = request.form.get('target_group', 'General Church')
        bible_version = request.form.get('bible_version', 'KJV')
        question_type = request.form.get('question_type', 'Mixed')
        source_type = request.form['source_type']
        count = int(request.form.get('count', 10))

        try:
            if source_type == 'topic_text':
                text = request.form.get('bible_text', '')

                difficulty = request.form.get('difficulty', 'Medium')
                question_style = request.form.get('question_style', 'Knowledge')

                source_material = f"""
Bible Passage / Topic / Theme:
{text}

Bible Version:
{bible_version}

Question Type:
{question_type}

Question Style:
{question_style}

Question Style Guidelines:
- Knowledge: Focus on biblical facts, events, people, places, teachings, and Scripture understanding.
- Application: Focus on applying biblical principles to daily Christian life, decision-making, character, and faith practice.
- Spiritual Reflection: Focus on personal devotion, spiritual growth, prayer, transformation, and relationship with God.


Question Style:
{question_style}

Question Style Guidelines:
- Knowledge: Focus on biblical facts, events, people, places, teachings, and Scripture understanding.
- Application: Focus on applying biblical principles to daily Christian life, decision-making, character, and faith practice.
- Spiritual Reflection: Focus on personal devotion, spiritual growth, prayer, transformation, and relationship with God.


Difficulty:
{difficulty}

Question Style:
{question_style}

Question Style Guidelines:
- Knowledge: Focus on biblical facts, events, people, places, teachings, and Scripture understanding.
- Application: Focus on applying biblical principles to daily Christian life, decision-making, character, and faith practice.
- Spiritual Reflection: Focus on personal devotion, spiritual growth, prayer, transformation, and relationship with God.

"""
            elif source_type == 'pasted_text':
                source_material = request.form.get('pasted_text', '')
            elif source_type == 'youtube':
                youtube_url = request.form.get('youtube_url', '')
                source_material = ai_generator.source_text_from_youtube(youtube_url)
            else:
                source_material = request.form.get('pasted_text', '')
        except Exception as exc:
            flash(f'Could not read source material: {exc}', 'error')
            return redirect(url_for('bible_quiz.new_quiz'))

        result = spend_units(100)
        if result is not True:
            return result

        from .fal_quiz_service import generate_quiz_with_fal
        import json
        import re

        questions = []
        status = "fal"

        fal_prompt = f"""
Create {count} Bible quiz questions for a church ministry.

Bible Passage / Topic / Theme:
{source_material}

Audience Age Group:
{age_group}

Generation Guidelines:
- Adjust vocabulary, complexity, and depth according to the selected audience.
- Children (6-12): Use simple biblical facts, memory-friendly questions, and clear language.
- Teenagers (13-19): Focus on faith challenges, identity, choices, and practical Christian living.
- Youth (20-35): Emphasize discipleship, decision-making, leadership, and life application.
- Adults (36+): Provide deeper biblical understanding and practical spiritual growth.
- Pastors / Church Leaders: Include theological insight, ministry leadership, and biblical interpretation.
- Seminary Students: Include exegetical depth, theological concepts, and biblical analysis.
- Mixed Congregation: Balance accessibility with spiritual depth.

Difficulty Level:
{difficulty}

Difficulty Guidelines:
- Beginner: Create simple questions focused on Bible facts, names, events, memory verses, and basic understanding.
- Medium: Create questions that test comprehension, biblical principles, spiritual application, and Christian living.
- Advanced: Create deeper questions involving context, interpretation, doctrine, connections between passages, and critical thinking.
- Theological / Seminary: Create scholarly questions involving biblical interpretation, theology, hermeneutics, historical background, and where appropriate original language insights.


Ministry Target Group:
{target_group}

Bible Version:
{bible_version}

Question Type:
{question_type}

Question Style:
{question_style}

Question Style Guidelines:
- Knowledge: Focus on biblical facts, events, people, places, teachings, and Scripture understanding.
- Application: Focus on applying biblical principles to daily Christian life, decision-making, character, and faith practice.
- Spiritual Reflection: Focus on personal devotion, spiritual growth, prayer, transformation, and relationship with God.


Instruction:
Generate questions that promote biblical knowledge, spiritual understanding,
practical application, and Christian growth.

Return ONLY JSON array:
[
 {{
  "text": "Question",
  "options": ["A","B","C","D"],
  "correct_index": 0,
  "scripture_ref": "Bible Reference",
  "explanation": "Biblical explanation",
  "difficulty": "Medium"
 }}
]
"""

        fal_result = generate_quiz_with_fal(fal_prompt)

        try:
            cleaned = re.sub(r'```json|```', '', fal_result).strip()
            questions = json.loads(cleaned)
        except Exception:
            questions = []

        if not questions:
            questions, status = ai_generator.generate_questions(
                source_material,
                age_group=age_group,
                count=count,
                target_group=target_group,
              bible_version=bible_version,
              question_type=question_type,
              difficulty=difficulty,
              question_style=question_style,
            )


        # Convert Fal AI JSON format to internal quiz format
        if questions and isinstance(questions, str):
            import json
            try:
                cleaned = questions.replace("```json", "").replace("```", "").strip()
                questions = json.loads(cleaned)
            except Exception:
                questions = []

        if isinstance(questions, dict):
            questions = [questions]

        converted_questions = []

        for q in questions:
            if "question" in q:
                answer = q.get("answer", "")
                options = q.get("options", [])

                converted_questions.append({
                    "text": q.get("question", ""),
                    "options": options,
                    "correct_index": options.index(answer) if answer in options else 0,
                    "scripture_ref": q.get("reference", ""),
                    "explanation": "Generated by Fal AI",
                    "difficulty": "Medium"
                })
            else:
                converted_questions.append(q)

        questions = converted_questions

        if not questions:
            refund_units(100)
            flash('Question generation failed. Your 10 Units have been refunded.', 'error')
            return redirect(url_for('bible_quiz.new_quiz'))

        quiz = BibleQuiz(
            owner_id=current_user.id,

              ministry_id=(
                  current_user.ministry_profile.id
                  if current_user.ministry_profile
                  else None
              ),
            title=title,
            age_group=age_group,
              target_group=target_group,
              bible_version=bible_version,
              question_type=question_type,
              difficulty=difficulty,
            source_type=source_type,
            source_ref=source_material[:2000],
        )
        db.session.add(quiz)
        db.session.flush()

        print("DEBUG QUESTIONS:", questions)

        for i, q in enumerate(questions):
            print("DEBUG QUESTION ITEM:", q)

            question = QuizQuestion(
                quiz_id=quiz.id,
                text=q['text'],
                correct_index=q['correct_index'],
                scripture_ref=q.get('scripture_ref', ''),
                explanation=q.get('explanation', ''),
                difficulty=q.get('difficulty', 'Medium'),

                # AI Intelligence Metadata
                age_group=q.get('age_group', quiz.age_group),
                target_group=q.get('target_group', quiz.target_group),
                question_style=q.get('question_style', quiz.question_style),
                question_type=q.get('question_type', quiz.question_type),
                ai_generated=(status == 'ai'),

                order_index=i,
            )
            question.options = q['options']
            db.session.add(question)

        try:
            db.session.commit()
            print("DEBUG: QUIZ SAVED SUCCESSFULLY ID:", quiz.id)
        except Exception as e:
            db.session.rollback()
            print("DEBUG DATABASE ERROR:", repr(e))
            raise

        if status.startswith('fallback'): 
            flash(
                'AI generation was unavailable, so questions were pulled from the '
                'built-in fallback bank. You can edit them below.',
                'warning',
            )
        else:
            flash(f'Generated {len(questions)} questions. Review and edit below.', 'success')

        return redirect(url_for('bible_quiz.edit_quiz', quiz_id=quiz.id))

    ministry = getattr(current_user, "ministry_profile", None)
    return render_template(
        'bible_quiz/new_quiz.html',
        ministry=ministry
    )


@bible_quiz_bp.route('/<int:quiz_id>/delete', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    print("DELETE QUIZ REQUEST RECEIVED:", quiz_id)

    quiz = BibleQuiz.query.filter_by(
        id=quiz_id,
        owner_id=current_user.id
    ).first_or_404()

    db.session.delete(quiz)
    db.session.commit()

    flash('Quiz deleted successfully.', 'success')
    return redirect(url_for('bible_quiz.dashboard'))


@bible_quiz_bp.route('/<int:quiz_id>/edit')
@login_required
def edit_quiz(quiz_id):
    quiz = BibleQuiz.query.filter_by(id=quiz_id, owner_id=current_user.id).first_or_404()
    return render_template('bible_quiz/edit_quiz.html', quiz=quiz)



@bible_quiz_bp.route('/<int:quiz_id>/update-settings', methods=['POST'])
@login_required
def update_quiz_settings(quiz_id):
    quiz = BibleQuiz.query.filter_by(id=quiz_id, owner_id=current_user.id).first_or_404()

    quiz.target_group = request.form.get('target_group', quiz.target_group)
    quiz.bible_version = request.form.get('bible_version', quiz.bible_version)
    quiz.question_type = request.form.get('question_type', quiz.question_type)
    quiz.difficulty = request.form.get('difficulty', quiz.difficulty)
    quiz.question_style = request.form.get('question_style', quiz.question_style)

    db.session.commit()

    flash('Quiz settings updated successfully.', 'success')
    return redirect(url_for('bible_quiz.edit_quiz', quiz_id=quiz.id))

@bible_quiz_bp.route('/<int:quiz_id>/question/<int:question_id>/update', methods=['POST'])
@login_required
def update_question(quiz_id, question_id):
    question = QuizQuestion.query.get_or_404(question_id)
    data = request.get_json()
    question.text = data.get('text', question.text)
    if 'options' in data:
        question.options = data['options']
    if 'correct_index' in data:
        question.correct_index = int(data['correct_index'])
    db.session.commit()
    return jsonify({'ok': True})


@bible_quiz_bp.route('/<int:quiz_id>/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(quiz_id, question_id):
    question = QuizQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'ok': True})


@bible_quiz_bp.route('/report/<int:session_id>')
@login_required
def quiz_report(session_id):
    session = QuizLiveSession.query.get_or_404(session_id)

    participants = QuizParticipant.query.filter_by(
        session_id=session_id
    ).order_by(
        QuizParticipant.score.desc()
    ).all()

    total_participants = len(participants)

    total_questions = len(
        session.quiz.questions
    )

    answers = QuizAnswer.query.join(
        QuizParticipant
    ).filter(
        QuizParticipant.session_id == session_id
    ).all()

    total_answers = len(answers)

    correct_answers = len([
        a for a in answers
        if a.is_correct
    ])

    accuracy = 0

    if total_answers:
        accuracy = round(
            (correct_answers / total_answers) * 100,
            1
        )

    return render_template(
        'bible_quiz/report.html',
        session=session,
        participants=participants,
        total_participants=total_participants,
        total_questions=total_questions,
        total_answers=total_answers,
        correct_answers=correct_answers,
        accuracy=accuracy
    )


@bible_quiz_bp.route('/analytics/data')
@login_required
def quiz_analytics_data():

    from sqlalchemy import func

    # Get quizzes owned by current user or ministry
    ministry = getattr(
        current_user,
        "ministry_profile",
        None
    )

    if ministry:
        quiz_ids = [
            q.id for q in BibleQuiz.query.filter_by(
                ministry_id=ministry.id
            ).all()
        ]
    else:
        quiz_ids = [
            q.id for q in BibleQuiz.query.filter_by(
                owner_id=current_user.id
            ).all()
        ]


    questions = QuizQuestion.query.filter(
        QuizQuestion.quiz_id.in_(quiz_ids)
    ).all()


    total_questions = len(questions)

    ai_generated = len([
        q for q in questions
        if getattr(q, "ai_generated", False)
    ])

    fallback = total_questions - ai_generated


    difficulty = {}

    for q in questions:
        level = q.difficulty or "Unknown"
        difficulty[level] = difficulty.get(level, 0) + 1


    styles = {}

    for q in questions:
        style = q.question_style or "Unknown"
        styles[style] = styles.get(style, 0) + 1


    age_groups = {}

    for q in questions:
        age = q.age_group or "Unknown"
        age_groups[age] = age_groups.get(age, 0) + 1


    target_groups = {}

    for q in questions:
        target = q.target_group or "Unknown"
        target_groups[target] = target_groups.get(target, 0) + 1


    return jsonify({

        "total_questions": total_questions,

        "ai_generated": ai_generated,

        "fallback": fallback,

        "difficulty": difficulty,

        "styles": styles,

        "age_groups": age_groups,

        "target_groups": target_groups

    })
