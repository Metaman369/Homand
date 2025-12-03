from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# GEMINI_API_KEY از .env خوانده می‌شود
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

@app.route("/", methods=["POST"])
def forward_to_gemini():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    gemini_url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {"parts": [{"text": user_message}]}
        ]
    }

    r = requests.post(gemini_url, json=payload)

    try:
        result = r.json()
        return jsonify(result)
    except:
        return jsonify({"error": "Invalid response from Gemini"}), 500


@app.route("/", methods=["GET"])
def home():
    return "Gemini Forwarder is running! 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
