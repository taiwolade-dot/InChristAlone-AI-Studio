import requests
import time
from flask import current_app

FAL_LLM_URL = "https://queue.fal.run/fal-ai/any-llm"

def generate_quiz_with_fal(prompt, model="google/gemini-2.5-flash"):
    api_key = current_app.config.get("FAL_API_KEY")
    if not api_key:
        print("No FAL_API_KEY configured")
        return None

    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "prompt": prompt,
    }

    try:
        r = requests.post(
            FAL_LLM_URL,
            json=payload,
            headers=headers,
            timeout=60,
        )

        print("SUBMIT STATUS:", r.status_code)
        print("SUBMIT RESPONSE:", r.text)

        if r.status_code != 200:
            return None

        data = r.json()

        # synchronous response
        if "text" in data:
            return data["text"]

        status_url = data.get("status_url")
        response_url = data.get("response_url")

        if not status_url or not response_url:
            print("No queue URLs returned.")
            return None

        for i in range(30):
            time.sleep(1)

            s = requests.get(
                status_url,
                headers=headers,
                timeout=30,
            )

            status = s.json()

            print(f"POLL {i+1}:", status)

            if status.get("status") == "COMPLETED":
                result = requests.get(
                    response_url,
                    headers=headers,
                    timeout=30,
                )

                print("FINAL JSON:")
                print(result.text)

                try:
                    final_data = result.json()
                    print("FINAL DATA PARSED:")
                    print(final_data)

                    if isinstance(final_data, dict):
                        if final_data.get("output"):
                            return final_data["output"]

                        if final_data.get("text"):
                            return final_data["text"]

                        if final_data.get("response"):
                            return final_data["response"]

                        if final_data.get("output_text"):
                            return final_data["output_text"]

                    return str(final_data)
                except Exception:
                    return result.text

            if status.get("status") == "ERROR":
                print("Fal job failed.")
                return None

        print("Timed out waiting for Fal response.")
        return None

    except Exception as e:
        print("ERROR:", e)
        return None
