import requests
from flask import current_app

FAL_QUEUE_URL = "https://queue.fal.run/fal-ai/flux/schnell"


def generate_image(prompt_text):
    """
    Calls fal.ai's Flux Schnell model to generate a real image from a text prompt.
    Returns the image URL on success, or None on failure (fails silently so
    the app falls back to showing the text prompt instead).
    """
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None

    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt_text,
        "image_size": "square_hd",
        "num_images": 1,
    }

    try:
        # Submit the generation request to the queue
        response = requests.post(FAL_QUEUE_URL, json=payload, headers=headers, timeout=30)
        print("========== FAL DEBUG ==========")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        if response.status_code != 200:
            return None

        data = response.json()

        # Some fal endpoints respond synchronously with images directly
        if "images" in data and len(data["images"]) > 0:
            return data["images"][0]["url"]

        # Otherwise, it's a queued request - poll for the result
        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")

        if not request_id:
            return None

        import time
        for _ in range(20):  # poll up to ~20 seconds
            time.sleep(1)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                if "images" in result_data and len(result_data["images"]) > 0:
                    return result_data["images"][0]["url"]
                return None
            elif status_data.get("status") == "ERROR":
                return None

        return None  # timed out waiting

    except requests.RequestException:
        return None

FAL_UPSCALE_URL = "https://queue.fal.run/fal-ai/esrgan"


def upscale_image(image_url, scale=2):
    """
    Calls fal.ai's ESRGAN model to upscale an existing image URL.
    Returns the upscaled image URL on success, or None on failure.
    """
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None

    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "image_url": image_url,
        "scale": scale,
    }

    try:
        response = requests.post(FAL_UPSCALE_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return None

        data = response.json()

        if "image" in data and isinstance(data["image"], dict):
            return data["image"].get("url")

        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")

        if not request_id:
            return None

        import time
        for _ in range(20):
            time.sleep(1)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                if "image" in result_data and isinstance(result_data["image"], dict):
                    return result_data["image"].get("url")
                return None
            elif status_data.get("status") == "ERROR":
                return None

        return None

    except requests.RequestException:
        return None

FAL_EDIT_URL = "https://queue.fal.run/fal-ai/flux-kontext-lora"


def edit_image(image_data_uri, prompt_text):
    """
    Calls fal.ai's Flux Kontext model to edit an uploaded image based on
    a text instruction (e.g. "change the background to a natural outdoor scene").
    image_data_uri should be a base64 data URI (data:image/...;base64,...).
    Returns the edited image URL on success, or None on failure.
    """
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None

    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "image_url": image_data_uri,
        "prompt": prompt_text,
    }

    try:
        response = requests.post(FAL_EDIT_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return None

        data = response.json()

        if "images" in data and len(data["images"]) > 0:
            return data["images"][0]["url"]

        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")

        if not request_id:
            return None

        import time
        for _ in range(25):
            time.sleep(1)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                if "images" in result_data and len(result_data["images"]) > 0:
                    return result_data["images"][0]["url"]
                return None
            elif status_data.get("status") == "ERROR":
                return None

        return None

    except requests.RequestException:
        return None


FAL_VIDEO_URL = "https://queue.fal.run/fal-ai/veo3.1/fast"


def generate_video(prompt_text, duration=5):
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt_text,
        "generate_audio": True,
        "resolution": "720p",
    }
    try:
        response = requests.post(FAL_VIDEO_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        data = response.json()
        if "video" in data and isinstance(data["video"], dict):
            return data["video"].get("url")
        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")
        if not request_id:
            return None
        import time
        for _ in range(90):
            time.sleep(2)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                if "video" in result_data and isinstance(result_data["video"], dict):
                    return result_data["video"].get("url")
                return None
            elif status_data.get("status") == "ERROR":
                return None
        return None
    except requests.RequestException:
        return None


FAL_MUSIC_URL = "https://queue.fal.run/fal-ai/minimax-music/v2"


def generate_music(style_prompt, lyrics):
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": style_prompt[:300],
        "lyrics_prompt": lyrics[:3000],
    }
    try:
        response = requests.post(FAL_MUSIC_URL, json=payload, headers=headers, timeout=30)
        print("FAL MUSIC STATUS:", response.status_code)
        print("FAL MUSIC BODY:", response.text[:500])
        if response.status_code != 200:
            return None
        data = response.json()
        if "audio" in data and isinstance(data["audio"], dict):
            return data["audio"].get("url")
        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")
        if not request_id:
            return None
        import time
        for _ in range(60):
            time.sleep(2)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            print("FAL MUSIC POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                print("FAL MUSIC RESULT:", result_data)
                if "audio" in result_data and isinstance(result_data["audio"], dict):
                    return result_data["audio"].get("url")
                return None
            elif status_data.get("status") == "ERROR":
                print("FAL MUSIC ERROR STATUS:", status_data)
                return None
        return None



    except requests.RequestException:
        return None


FAL_VOICE_URL = "https://queue.fal.run/fal-ai/kokoro/american-english"


def generate_voice(text, voice="af_heart"):
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": text[:2000],
        "voice": voice,
    }
    try:
        response = requests.post(FAL_VOICE_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        data = response.json()
        if "audio" in data and isinstance(data["audio"], dict):
            return data["audio"].get("url")
        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")
        if not request_id:
            return None
        import time
        for _ in range(30):
            time.sleep(1)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                if "audio" in result_data and isinstance(result_data["audio"], dict):
                    return result_data["audio"].get("url")
                return None
            elif status_data.get("status") == "ERROR":
                return None
        return None
    except requests.RequestException:
        return None


FAL_TRANSCRIBE_URL = "https://queue.fal.run/fal-ai/wizper"


def transcribe_audio(audio_data_uri):
    api_key = current_app.config.get('FAL_API_KEY')
    if not api_key:
        return None
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "audio_url": audio_data_uri,
        "task": "transcribe",
    }
    try:
        response = requests.post(FAL_TRANSCRIBE_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        data = response.json()
        if "text" in data:
            return data.get("text")
        request_id = data.get("request_id")
        status_url = data.get("status_url")
        response_url = data.get("response_url")
        if not request_id:
            return None
        import time
        for _ in range(45):
            time.sleep(2)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            status_data = status_resp.json()
            print("FAL POLL:", status_data)
            if status_data.get("status") == "COMPLETED":
                result_resp = requests.get(response_url, headers=headers, timeout=15)
                result_data = result_resp.json()
                print("FAL RESULT:", result_data)
                if "text" in result_data:
                    return result_data.get("text")
                return None
            elif status_data.get("status") == "ERROR":
                return None
        return None
    except requests.RequestException:
        return None
