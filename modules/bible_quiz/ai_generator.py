FALLBACK_BANK = [
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

def generate_questions(source_material, age_group="Youth", count=10):
    import os, json
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Generate {count} multiple choice Bible quiz questions for {age_group} from this text: {source_material}. Return ONLY JSON list with keys: text, options (list of 4 strings), correct_index (0-3), scripture_ref, explanation, difficulty."
            resp = model.generate_content(prompt)
            text = resp.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            data = json.loads(text)
            if isinstance(data, list) and len(data) > 0:
                return data[:count], "ai"
        except Exception as e:
            print("AI Generation failed:", e)

    selected = []
    for i in range(count):
        selected.append(FALLBACK_BANK[i % len(FALLBACK_BANK)])
    return selected, "fallback"
