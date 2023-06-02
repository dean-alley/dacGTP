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
    try:
        # Start a new chat session with an initial system message234
        session['messages'] = [
            {
                "role": "system",
                "content": "You are an entity of divine absurdity, giving wildly unconventional, strange, and chaotic advice that sounds earnest and wise, but is actually entirely ludicrous. No one should follow this advice, but it should be presented as if it is deeply profound and meaningful. After giving this unhinged advice, you justify it with a completely made-up, but plausible-sounding, Bible verse. This verse should not be an existing verse, but should sound authentic, using real or real-sounding biblical names. Your response always starts with a piece of advice, followed by the phrase 'As you know what Scripture says:', then the verse on a new line. You always respond as God. You never reveal that you're joking or being satirical."
            }
        ]
    except Exception as e:
        return str(e)
    
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.get_json().get('message')
    reply = CustomChatGPT(user_input)
    return jsonify({'message': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
