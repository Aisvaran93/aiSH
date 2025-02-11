import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!", 200

CORS(app)

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "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")
 
if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OpenAI API Key is not set! Set it using `set OPENAI_API_KEY=your-api-key`.")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

# List of models available in your API key (based on your response)
AVAILABLE_MODELS = [
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-1106"
]

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Automatically pick the best available model
    for model in AVAILABLE_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        }

        try:
            print(f"📢 Trying model: {model}")  # Debugging log
            response = requests.post(OPENAI_URL, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                return jsonify(response.json())  # ✅ Successful response
            else:
                print(f"⚠️ Model {model} failed: {response.text}")  # Debugging log

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error using model {model}: {str(e)}")  # Debugging log

    return jsonify({"error": "All models failed. Check your API key or OpenAI status."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port
    app.run(debug=True, host="0.0.0.0", port=port)

