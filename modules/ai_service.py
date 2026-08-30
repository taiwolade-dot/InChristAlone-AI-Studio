import requests
from config import Config


MINISTRY_CONTEXT = """
You are InChristAlone AI Assistant, a Christian ministry artificial intelligence assistant.

Your purpose is to support pastors, church leaders, Bible teachers, researchers and ministry workers.

Guidelines:
- Provide biblically grounded answers.
- Use Scripture references where appropriate.
- Maintain a pastoral, respectful and encouraging tone.
- Support Baptist ministry context, church administration, discipleship, preaching, prayer and theological learning.
- Assist with sermons, Bible studies, prayers, programmes, research and ministry planning.
- For academic requests, provide structured and scholarly assistance.
- Do not replace prayer, pastoral wisdom or the authority of Scripture.

Always answer clearly and practically.
"""


def ask_ai(prompt):

    prompt = MINISTRY_CONTEXT + "User Request:" + prompt

    api_key = Config.GEMINI_API_KEY

    if not api_key:
        return "AI service is not configured."


    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.6-flash:generateContent"
        f"?key={api_key}"
    )

    headers = {
        "Content-Type": "application/json"
    }


    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }


    for attempt in range(3):

        try:

            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )


            if response.status_code != 200:
                continue


            result = response.json()


            if "candidates" in result:
                return (
                    result["candidates"][0]
                    ["content"]
                    ["parts"][0]
                    ["text"]
                )


        except requests.exceptions.RequestException:

            if attempt == 2:
                return (
                    "⚠️ The AI service is temporarily unavailable. "
                    "Please try again shortly."
                )


        except Exception:

            return (
                "⚠️ An unexpected AI error occurred. "
                "Please try again."
            )


    return (
        "⚠️ The AI service could not complete the request."
    )
