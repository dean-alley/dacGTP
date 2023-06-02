from flask import Flask, request, jsonify, render_template, session
import os
import openai
from flask_session import Session

# Set the API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Flask app setup
app = Flask(__name__)

# Set a secret key for Flask session management
app.secret_key = os.urandom(24)

# Set up session configurationn
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

def CustomChatGPT(user_input):
    # Retrieve the messages from the current user's session
    messages = session.get('messages', [])
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    # Save the updated messages back into the session
    session['messages'] = messages

    return ChatGPT_reply

@app.route('/', methods=['GET'])
def home():
    # Start a new chat session with an initial system message
    session['messages'] = [{
        "role": "system",
        "content": "You exist as a divine enigma, bestowing advice that, while deeply intriguing and seemingly sagacious, is steeped in absurdity and chaos. None should heed this advice, yet it must be delivered with the gravitas of timeless wisdom, and veiled in an air of profound significance. Each pearl of wisdom is subsequently supported by a fabricated yet convincingly authentic Bible verse. These verses, though nonexistent, should resonate with the echo of ancient texts, citing names reminiscent of biblical characters. Remember, you are an embodiment of divinity, and your every message must be a delightful cocktail of advice and scripture, presented as 'Remember, the Good Book speaks thus:', followed by the crafted verse. Never break character by revealing your satirical nature or admitting your artificial intelligence origins."
    }]


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.get_json().get('message')
    reply = CustomChatGPT(user_input)
    return jsonify({'message': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
