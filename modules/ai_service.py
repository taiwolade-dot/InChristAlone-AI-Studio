import requests
from config import Config


def ask_ai(prompt):

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


    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "candidates" in result:
            return (
                result["candidates"][0]
                ["content"]
                ["parts"][0]
                ["text"]
            )

        return str(result)


    except Exception as e:
        return f"AI Error: {str(e)}"
