from flask import Flask, render_template, request
import whisper
from langdetect import detect
import os

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio_file']
    if audio_file:
        # Save the audio file to a temporary location
        audio_path = os.path.join(app.root_path, 'temp.mp3')
        audio_file.save(audio_path)

        # Detect the language of the audio file
        detected_language = detect_language(audio_path)

        # Transcribe the audio
        result = model.transcribe(audio_path, language=detected_language)
        transcribed_text = result["text"]

        # Read the audio data
        with open(audio_path, "rb") as f:
            audio_data = f.read()

        # Remove the temporary audio file
        os.remove(audio_path)

        return render_template('index1.html', success=True, text=transcribed_text, detected_language=detected_language, audio_data=audio_data)
    else:
        return render_template('index1.html', error="No audio file provided")

def detect_language(audio_path):
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    try:
        detected_language = detect(audio_data)
    except Exception as e:
        print(f"Error detecting language: {e}")
        detected_language = "unknown"

    if detected_language == "unknown":
        # Set a default language if language detection fails
        detected_language = "english"

    return detected_language

if __name__ == '__main__':
    app.run(debug=True)

