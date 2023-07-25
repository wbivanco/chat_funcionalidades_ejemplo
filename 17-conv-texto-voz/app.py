from flask import Flask, render_template, request, jsonify
import pyttsx3
import threading

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    threading.Thread(target=speak_async, args=(text,)).start()
    return jsonify(success=True)


def speak_async(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.setProperty("voice", "spanish")
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    app.run(debug=True)
