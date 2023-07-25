# Librerías para Chatbot
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os


load_dotenv()  
openai_key = os.getenv('OPENAI_API_KEY')
                    
                    
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    openai.api_key = openai_key

    prompt = request.json.get('message', '')

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0
    )

    ai_message = response['choices'][0]['text']
    return jsonify({'message': ai_message})


if __name__ == '__main__':
    app.run(debug=True)
