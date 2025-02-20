import os
import tempfile
import werkzeug
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!", 200

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OpenAI API Key is not set! Add it in Render's environment variables.")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"  # Set GPT-4o-mini as the default model

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    print(f"🚀 Using model: {DEFAULT_MODEL}", flush=True)  # Log model usage

    try:
        response = requests.post(OPENAI_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            response_data = response.json()
            response_data["model"] = DEFAULT_MODEL  # Explicitly show the model in response
            return jsonify(response_data)
        else:
            print(f"⚠️ OpenAI API error: {response.text}", flush=True)
            return jsonify({"error": "OpenAI API error"}), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API Request Error: {str(e)}", flush=True)
        return jsonify({"error": "Server error. Try again later."}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        print(f"📥 Received request: {request}", flush=True)
        print(f"🔍 Request headers: {request.headers}", flush=True)
        print(f"📂 Request files: {request.files}", flush=True)

        if "file" not in request.files:
            print("⚠️ No file detected in request!", flush=True)
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        filename = werkzeug.utils.secure_filename(file.filename)  # Ensure filename is defined
        file_content = file.read()  # Read file into memory
        file_size = len(file_content)  # Get file size

        # Use a temporary directory for file storage (since Render's free tier does not support persistent storage)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)

        with open(file_path, "wb") as f:
            f.write(file_content)  # Save file in temporary location

        print(f"✅ File received: {filename}, Size: {file_size} bytes", flush=True)
        print(f"📂 File temporarily saved at: {file_path}", flush=True)

        return jsonify({
            "message": "File uploaded successfully!",
            "filename": filename,
            "size": file_size,
            "file_path": file_path  # Returning temp path for debugging
        })

    except Exception as e:
        print(f"❌ File Upload Error: {str(e)}", flush=True)
        return jsonify({"error": "File upload failed", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
