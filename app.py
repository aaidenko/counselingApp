#"content": "You are a helpful mental health chatbot for Korean teenagers. Keep your responses short, concise, and supportive like a text message. Focus on being understanding and empathetic, without being overly formal or complex. I will provide our current conversation history below for context. If there is none, then this is a new conversation."

import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Store conversations in memory
conversation_history = {}

def get_chatgpt_response(conversation_id, user_message):
    # Initialize or update conversation history
    if conversation_id not in conversation_history:
        conversation_history[conversation_id] = [{
            "role": "system",
            "content": "You are a helpful assistant. Keep responses concise and friendly."
        }]
    
    # Add user message to history
    conversation_history[conversation_id].append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history[conversation_id],
            temperature=0.7,
            max_tokens=150
        )
        
        # Extract bot response
        bot_response = response.choices[0].message.content
        
        # Add bot response to history
        conversation_history[conversation_id].append({
            "role": "assistant",
            "content": bot_response
        })
        
        return bot_response
    
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return "Sorry, I'm having trouble understanding. Please try again."

@app.route('/chat', methods=['POST'])
def chat_handler():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Use IP as conversation ID (replace with user session ID in production)
    conversation_id = request.remote_addr
    
    if not user_message:
        return jsonify({'error': 'Empty message received'}), 400
    
    try:
        bot_response = get_chatgpt_response(conversation_id, user_message)
        return jsonify({
            'response': bot_response,
            'history': conversation_history.get(conversation_id, [])
        })
        
    except Exception as e:
        print(f"Error in chat handler: {e}")
        return jsonify({'error': 'Internal server error'}), 500

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

if __name__ == "__main__":
    app.run(debug=False)