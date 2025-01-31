#"content": "You are a helpful mental health chatbot for Korean teenagers. Keep your responses short, concise, and supportive like a text message. Focus on being understanding and empathetic, without being overly formal or complex. I will provide our current conversation history below for context. If there is none, then this is a new conversation."

import os
import openai
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Serve the root URL (e.g., '/') with index.html
@app.route('/')
def index():
    return render_template('index.html')

# Dynamically handle all other .html requests
@app.route('/<path:page>.html')
def serve_html(page):
    return render_template(f'{page}.html')

# Serve CSS files from /css/* paths
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

# Serve JS files from /js/* paths
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

# Serve images from /images/* paths
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

# Chatbot API route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # OpenAI API request
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False)