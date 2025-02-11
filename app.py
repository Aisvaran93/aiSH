import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!", 200

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OpenAI API Key is not set! Add it in Render's environment variables.")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o-mini-2024-07-18", "gpt-3.5-turbo", "gpt-3.5-turbo-1106"]

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "")
    uploaded_file = request.files.get("file")

    # Handle File Upload
    if uploaded_file:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"response": f"📁 File '{uploaded_file.filename}' uploaded successfully!"})

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
            response = requests.post(OPENAI_URL, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                return jsonify(response.json())
            else:
                print(f"⚠️ Model {model} failed: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error using model {model}: {str(e)}")

    return jsonify({"error": "All models failed. Check your API key or OpenAI status."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
