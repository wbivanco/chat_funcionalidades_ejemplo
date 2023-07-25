from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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

    return render_template('index.html', transcript=transcript)


if __name__ == '__main__':
    app.run(debug=True)
