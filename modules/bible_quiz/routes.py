from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from models import db, BibleQuiz, QuizQuestion
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
    quizzes = BibleQuiz.query.filter_by(owner_id=current_user.id).order_by(
        BibleQuiz.created_at.desc()
    ).all()
    return render_template('bible_quiz/dashboard.html', quizzes=quizzes)


@bible_quiz_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_quiz():
    from modules.wallet_utils import spend_units, refund_units

    if request.method == 'POST':
        title = request.form['title'].strip()
        age_group = request.form['age_group']
        source_type = request.form['source_type']
        count = int(request.form.get('count', 10))

        try:
            if source_type == 'topic_text':
                topic = request.form.get('topic', '')
                text = request.form.get('bible_text', '')
                source_material = f"Topic: {topic}\n\nText: {text}"
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

        result = spend_units(10)
        if result is not True:
            return result

        questions, status = ai_generator.generate_questions(
            source_material, age_group=age_group, count=count
        )

        if not questions:
            refund_units(10)
            flash('Question generation failed. Your 10 Units have been refunded.', 'error')
            return redirect(url_for('bible_quiz.new_quiz'))

        quiz = BibleQuiz(
            owner_id=current_user.id,
            title=title,
            age_group=age_group,
            source_type=source_type,
            source_ref=source_material[:2000],
        )
        db.session.add(quiz)
        db.session.flush()

        for i, q in enumerate(questions):
            question = QuizQuestion(
                quiz_id=quiz.id,
                text=q['text'],
                correct_index=q['correct_index'],
                scripture_ref=q.get('scripture_ref', ''),
                explanation=q.get('explanation', ''),
                difficulty=q.get('difficulty', 'Medium'),
                order_index=i,
            )
            question.options = q['options']
            db.session.add(question)

        db.session.commit()

        if status.startswith('fallback'):
            flash(
                'AI generation was unavailable, so questions were pulled from the '
                'built-in fallback bank. You can edit them below.',
                'warning',
            )
        else:
            flash(f'Generated {len(questions)} questions. Review and edit below.', 'success')

        return redirect(url_for('bible_quiz.edit_quiz', quiz_id=quiz.id))

    return render_template('bible_quiz/new_quiz.html')


@bible_quiz_bp.route('/<int:quiz_id>/edit')
@login_required
def edit_quiz(quiz_id):
    quiz = BibleQuiz.query.filter_by(id=quiz_id, owner_id=current_user.id).first_or_404()
    return render_template('bible_quiz/edit_quiz.html', quiz=quiz)


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
