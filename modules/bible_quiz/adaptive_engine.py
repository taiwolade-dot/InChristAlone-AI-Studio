from modules.bible_quiz.ai_generator import generate_questions


def regenerate_question(question, analytics):

    """
    Adaptive Bible Quiz Question Improvement Engine
    """

    accuracy = getattr(
        analytics,
        "accuracy_rate",
        100
    )


    # Determine new difficulty

    if accuracy < 40:
        difficulty = "Beginner"

        instruction = (
            "Simplify this question. "
            "Use clear Bible teaching language."
        )

    elif accuracy < 70:
        difficulty = "Medium"

        instruction = (
            "Maintain difficulty but improve clarity."
        )

    else:
        difficulty = "Advanced"

        instruction = (
            "Increase theological depth and challenge."
        )


    prompt_context = f"""
Original Question:
{question.text}

Scripture:
{question.scripture_ref}

Current difficulty:
{question.difficulty}

AI Instruction:
{instruction}

Generate an improved Bible quiz question.
"""


    questions, status = generate_questions(
        source_material=prompt_context,
        count=1,
        age_group=getattr(question, "age_group", "General"),
        target_group=getattr(question, "target_group", "General Church"),
        question_style=getattr(question, "question_style", "Knowledge"),
        question_type=getattr(question, "question_type", "Multiple Choice"),
        difficulty=difficulty
    )


    if questions:

        new_question = questions[0]

        return {
            "text": new_question.get("text"),
            "options": new_question.get("options"),
            "correct_index": new_question.get("correct_index"),
            "scripture_ref": new_question.get("scripture_ref"),
            "explanation": new_question.get("explanation"),
            "difficulty": difficulty,
            "ai_generated": True
        }


    return None
