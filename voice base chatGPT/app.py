from flask import Flask, request, jsonify,render_template,send_from_directory
from gtts import gTTS
import openai
from flask_cors import CORS
from config import apikey



app = Flask(__name__)
CORS(app)



openai.api_key = apikey

def openais(message):
    res = openai.Completion.create(
                model="text-davinci-003",
                prompt=message,
                max_tokens=50,
                temperature=0.6,
            )
    r = res.choices[0].text 
    return r


@app.route('/')
def index():
    return render_template('voice.html')

@app.route('/transcript', methods=['POST'])
def transcribe():
    transcript = request.json['transcript']
    print(transcript)
    res = openais(transcript)
    tts = gTTS(res)
    audio_file = 'audio.mp3'
    tts.save(audio_file)
    return jsonify({'audio_file': audio_file,'text':res})

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
