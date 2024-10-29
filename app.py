import streamlit as st
from flask import Flask, request, jsonify, render_template
from threading import Thread
import requests

# Initialize Flask app
app = Flask(__name__)

API_KEY = 'sk-4qBNWVVpOBFDmM_7XNBpwYtc0PbOt_tpsIM0YeCaw1T3BlbkFJJNU5C8pgGWx0NGpi75ImeN0Yx4iAiXF9PPLJYOge0A'  # Replace with your actual OpenAI API key

# Flask Routes
@app.route('/')
def index():
    return "This endpoint is for the Flask API."

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'reply': 'Please provide a message.'}), 400

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': user_message}],
                'max_tokens': 150,
            }
        )

        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']
        return jsonify({'reply': bot_reply})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({'reply': 'An error occurred with the OpenAI API.'}), 500
    except Exception as e:
        return jsonify({'reply': 'An unexpected error occurred.'}), 500

# Function to run Flask
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Start Flask in a separate thread
thread = Thread(target=run_flask)
thread.start()

# Streamlit interface for testing
st.title("Streamlit with Flask API")
st.write("Use the form below to chat with the API")

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if user_input:
        response = requests.post("http://127.0.0.1:5000/api/chat", json={"message": user_input})
        if response.status_code == 200:
            st.write("Bot reply:", response.json().get("reply"))
        else:
            st.write("Error:", response.json().get("reply"))
    else:
        st.write("Please enter a message.")
