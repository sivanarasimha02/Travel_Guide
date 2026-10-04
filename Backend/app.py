import os
import base64
import tempfile
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Frontend"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

MURF_API_KEY = os.environ.get("MURF_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY" )

client = genai.Client(api_key=GEMINI_API_KEY)

PROMPTS = {
    "Summary": """
You are a professional tourist guide.
Provide a high-level overview of "{place}" in {language}.

Focus on:
- The historical significance
- Why the place is famous
- Key architectural or cultural highlights

Keep the explanation concise, engaging, and easy to follow.
Avoid excessive details and dates.
Limit the response to around 200 words.

Respond ONLY in {language}.
""",

    "Detailed": """
You are a professional tourist guide.
Provide a detailed and immersive explanation of "{place}" in {language}.

Cover:
- Historical background and timeline
- Architectural design and unique features
- Cultural importance and notable events
- Interesting facts and visitor insights

Explain concepts clearly and in a storytelling manner.
Include relevant details and examples to create a rich experience.
Limit the response to around 400 words.

Respond ONLY in {language}.
"""
}


def generate_speech(text, voice_id, locale):
    if not MURF_API_KEY or MURF_API_KEY == "YOUR_MURF_API_KEY_HERE":
        print("Warning: MURF_API_KEY is not configured.")
        return None

    url = "https://global.api.murf.ai/v1/speech/stream"
    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "voice_id": voice_id,
        "text": text,
        "locale": locale,
        "model": "FALCON",
        "format": "MP3",
        "sampleRate": 24000,
        "channelType": "MONO"
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            with open(temp_audio.name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("Audio streaming completed")
            return temp_audio.name
        else:
            print(f"Murf API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Speech generation error: {e}")
        return None


def generate_description(place, answer_type, language):
    prompt_template = PROMPTS.get(answer_type, PROMPTS["Summary"])
    prompt = prompt_template.format(place=place, language=language)

    # Try models with automatic fallback on temporary server capacity (503) errors
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    last_error = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            print(f"Model {model_name} encountered an issue ({e}). Retrying with alternate model...")

    raise last_error if last_error else RuntimeError("Failed to generate description")


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/generate-audio-guide", methods=["POST"])
def generate_audio_guide():
    data = request.get_json(silent=True) or {}
    place = data.get("place")
    answer_type = data.get("answerType", "Summary")
    language = data.get("language", "English")
    voice_id = data.get("voiceId")
    locale = data.get("locale")

    if not place:
        return jsonify({"error": "Destination 'place' is required"}), 400

    try:
        text_description = generate_description(place, answer_type, language)
    except Exception as e:
        print(f"Description generation error: {e}")
        return jsonify({"error": f"Failed to generate description: {str(e)}"}), 500

    encoded_audio = None
    if voice_id and locale:
        audio_path = generate_speech(text_description, voice_id, locale)
        if audio_path and os.path.exists(audio_path):
            try:
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                if audio_bytes:
                    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
            finally:
                try:
                    os.remove(audio_path)
                except OSError:
                    pass

    return jsonify({
        "description": text_description,
        "audioBase64": encoded_audio
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 Travel Guide running on http://127.0.0.1:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)