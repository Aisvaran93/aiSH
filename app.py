import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Flask API is running!"})

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OpenAI API Key is not set! Add it in Render's environment variables.")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o-mini-2024-07-18", "gpt-3.5-turbo", "gpt-3.5-turbo-1106"]

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

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
            ai_response = response.json()

            # 🔥 Debugging: Print entire OpenAI response
            print("🔍 OpenAI Response:", ai_response)

            if response.status_code == 200:
                if "choices" in ai_response and len(ai_response["choices"]) > 0:
                    return jsonify({"response": ai_response["choices"][0]["message"]["content"]})
                else:
                    return jsonify({"error": "Unexpected response format", "raw_response": ai_response}), 500

            else:
                print(f"⚠️ Model {model} failed: {ai_response}")
                continue  

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error using model {model}: {str(e)}")  

    return jsonify({"error": "All models failed. Check your API key or OpenAI status."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
