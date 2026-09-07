FALLBACK_BANK = [
# Each question includes adaptive metadata:
# age_group, target_group, question_style, question_type

    {"text": "How many books are in the New Testament?", "options": ["27", "39", "66", "12"], "correct_index": 0, "scripture_ref": "General", "explanation": "27 books.", "difficulty": "Easy"},
    {"text": "Which gospel was written by a doctor?", "options": ["Matthew", "Mark", "Luke", "John"], "correct_index": 2, "scripture_ref": "Col 4:14", "explanation": "Luke.", "difficulty": "Easy"},
    {"text": "Who was swallowed by a great fish?", "options": ["Daniel", "Jonah", "Elijah", "Noah"], "correct_index": 1, "scripture_ref": "Jonah 1:17", "explanation": "Jonah.", "difficulty": "Easy"},
    {"text": "What is the shortest verse in the Bible?", "options": ["Pray continuously", "Jesus wept", "God is love", "Rejoice evermore"], "correct_index": 1, "scripture_ref": "John 11:35", "explanation": "Jesus wept.", "difficulty": "Easy"},
    {"text": "Where was Jesus born?", "options": ["Nazareth", "Jerusalem", "Bethlehem", "Capernaum"], "correct_index": 2, "scripture_ref": "Matt 2:1", "explanation": "Bethlehem.", "difficulty": "Easy"},
    {"text": "Who was the first king of Israel?", "options": ["David", "Saul", "Solomon", "Samuel"], "correct_index": 1, "scripture_ref": "1 Sam 10:1", "explanation": "Saul.", "difficulty": "Medium"},
    {"text": "How many days was Lazarus in the tomb?", "options": ["1 day", "2 days", "3 days", "4 days"], "correct_index": 3, "scripture_ref": "John 11:39", "explanation": "4 days.", "difficulty": "Medium"},
    {"text": "What city walls collapsed after Israel marched around it?", "options": ["Ai", "Jericho", "Babylon", "Nineveh"], "correct_index": 1, "scripture_ref": "Joshua 6:20", "explanation": "Jericho.", "difficulty": "Easy"},
    {"text": "Who led the Israelites across the Red Sea?", "options": ["Moses", "Aaron", "Joshua", "Gideon"], "correct_index": 0, "scripture_ref": "Exodus 14:21", "explanation": "Moses.", "difficulty": "Easy"},
    {"text": "What is the first book of the Bible?", "options": ["Exodus", "Genesis", "Leviticus", "Psalms"], "correct_index": 1, "scripture_ref": "Genesis 1:1", "explanation": "Genesis.", "difficulty": "Easy"},
    {"text": "How many disciples did Jesus choose?", "options": ["7", "10", "12", "70"], "correct_index": 2, "scripture_ref": "Matt 10:1", "explanation": "12.", "difficulty": "Easy"},
    {"text": "What fruit of the Spirit is listed first in Galatians 5:22?", "options": ["Joy", "Peace", "Love", "Patience"], "correct_index": 2, "scripture_ref": "Gal 5:22", "explanation": "Love.", "difficulty": "Medium"},
    {"text": "Who wrote most of the New Testament epistles?", "options": ["Peter", "Paul", "John", "James"], "correct_index": 1, "scripture_ref": "Epistles", "explanation": "Paul.", "difficulty": "Easy"},
    {"text": "What river was Jesus baptized in?", "options": ["Nile", "Euphrates", "Jordan", "Tigris"], "correct_index": 2, "scripture_ref": "Matt 3:13", "explanation": "Jordan.", "difficulty": "Easy"},
    {"text": "Who received the Ten Commandments on Mount Sinai?", "options": ["Abraham", "Moses", "Elijah", "Jacob"], "correct_index": 1, "scripture_ref": "Exodus 20", "explanation": "Moses.", "difficulty": "Easy"}
]


# Default adaptive metadata for fallback questions
for q in FALLBACK_BANK:
    q.setdefault("age_group", "General")
    q.setdefault("target_group", "General Church")
    q.setdefault("question_style", "Knowledge")
    q.setdefault("question_type", "Multiple Choice")


def generate_questions(
    source_material,
    age_group="Youth",
    count=10,
    target_group="General Church",
    bible_version="KJV",
    question_type="Mixed",
    difficulty="Medium",
    question_style="Knowledge"
):
    import os, json
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
You are an expert Christian Bible teacher and quiz creator.

Generate {count} high-quality multiple choice Bible quiz questions.

Audience Age Group:
{age_group}

Ministry Target Group:
{target_group}

Bible Version:
{bible_version}

Question Type:
{question_type}

Difficulty Level:
{difficulty}

Question Style:
{question_style}

Source Material:
{source_material}

Requirements:
- Questions must be biblically accurate.
- Provide 4 answer options for each question.
- Only one option must be correct.
- Include Bible reference.
- Include a short explanation for the answer.
  - Match the selected difficulty level appropriately.
  - Adapt vocabulary, complexity, and depth according to the selected audience.
  - Follow the selected question style:
    - Knowledge: Focus on biblical facts, people, places, events, teachings, and Scripture understanding.
    - Application: Focus on Christian living, decision-making, discipleship, character, and practical faith.
    - Spiritual Reflection: Focus on devotion, prayer, transformation, spiritual growth, and relationship with God.
  - Use the selected Bible version when quoting or referencing Scripture.
- Avoid ambiguous questions.
- Encourage Bible knowledge and spiritual learning.

Return ONLY valid JSON.

Format:
[
 {{
  "text": "Question",
  "options": ["A", "B", "C", "D"],
  "correct_index": 0,
  "scripture_ref": "Book Chapter:Verse",
  "explanation": "Explanation",
  "difficulty": "Easy"
 }}
]
"""
            resp = model.generate_content(prompt)
            text = resp.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            data = json.loads(text)
            if isinstance(data, list) and len(data) > 0:
                return data[:count], "ai"
        except Exception as e:
            print("AI Generation failed:", e)

    # Adaptive fallback engine
    selected = []

    difficulty_map = {
        "Beginner": "Easy",
        "Medium": "Medium",
        "Advanced": "Medium",
        "Theological / Seminary": "Medium"
    }

    preferred_level = difficulty_map.get(
        difficulty,
        "Medium"
    )

    # Intelligent fallback scoring engine
    def question_score(q):
        score = 0

        # Difficulty matching
        if q.get("difficulty") == preferred_level:
            score += 5

        # Question style matching
        if q.get("question_style") == question_style:
            score += 4

        # Question type matching
        if q.get("question_type") == question_type:
            score += 3

        # Age group matching
        if q.get("age_group") == age_group:
            score += 3

        # Target group matching
        if q.get("target_group") == target_group:
            score += 2

        return score

    ranked = sorted(
        FALLBACK_BANK,
        key=question_score,
        reverse=True
    )

    for question in ranked:
        question = question.copy()

        question["age_group"] = age_group
        question["target_group"] = target_group
        question["question_style"] = question_style
        question["question_type"] = question_type

        selected.append(question)

        if len(selected) >= count:
            break

    # Fill remaining questions if bank is smaller
    while len(selected) < count:
        selected.append(
            FALLBACK_BANK[len(selected) % len(FALLBACK_BANK)]
        )

    return selected, "fallback"
