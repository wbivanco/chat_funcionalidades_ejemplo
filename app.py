# Librerías para carga de archivo .env
from dotenv import load_dotenv
import os
# Librerías para Chatbot
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
# Librerías para convertir de texto a voz
import pyttsx3
import threading
# Librerias para convertir de voz a texto
import speech_recognition as sr
from pydub import AudioSegment


# Inicializar app
app = Flask(__name__)
#CORS(app)

# Carga el API key de OpenAI
load_dotenv()  
openai_key = os.getenv('OPENAI_API_KEY')


### Carga pantalla de opciones ###
@app.route('/')
def index():
    return render_template('index.html')


### Chat ###
# Carga pantalla de chat
@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')


# Procesa chat
@app.route('/chat_procesar', methods=['POST'])
def chat_procesar():
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


### Imagen ###
# Carga pantalla de ingreso de prompt
@app.route('/imagen', methods=['GET'])
def imagen():
    return render_template('imagen.html')


# Procesa imagen
@app.route('/imagen_procesar', methods=['POST'])
def imagen_procesar():
    openai.api_key = openai_key

    prompt = request.json.get('message', '')

    response = openai.Image.create(    
        prompt=prompt,
        n=2,
        size='1024x1024'
    )
    ai_message = response['data'][0]['url']
    return jsonify({'message': ai_message})


### Texto a voz ###
# Carga pantalla de ingreso de texto
@app.route("/hablar")
def hablar():
    return render_template("convertir_tav.html")


@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    threading.Thread(target=speak_async, args=(text,)).start()
    return jsonify(success=True)

# Procesa el texto ingresado
def speak_async(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.setProperty("voice", "spanish")
    engine.say(text)
    engine.runAndWait()


### Voz a texto ###
# Transcribe el audio ingresado
@app.route('/transcribir', methods=['GET', 'POST'])
def transcribir():
    transcript = ""

    if request.method == 'POST':
        audio_file = request.files['file']
        audio_file.save("audio.wav")
        audio = AudioSegment.from_wav("audio.wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile("audio.wav") as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data, language='es-ES')
            except Exception as e:
                print(e)
                transcript = "Lo siento, no pude transcribir el audio."

    return render_template('convertir_vat.html', transcript=transcript)


if __name__ == '__main__':
    app.run(debug=True)
