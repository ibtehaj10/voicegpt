from flask import Flask, render_template,request
import requests
import speech_recognition as sr     # import the library
import subprocess 
# from gtts import gTTS
# from IPython.display import Audio
# from PIL import Image
import json
import random
import openai
import os
import time
from config import apikey
from flask import Flask, request, jsonify
from speech_recognition import Microphone, Recognizer

app = Flask(__name__)

openai.api_key = apikey

app = Flask (__name__)
app.config["CACHE_TYPE"] = "null"


@app.route('/')
def index():
    return render_template('voice.html')


@app.route('/recognize', methods=['POST'])
def recognize():
    audio_data = request.data
    print("Received audio data: ", audio_data) # Debug statement to check if audio data is received correctly
    # Initialize a new SpeechRecognition object
    recognizer = sr.Recognizer()
    # Convert the audio data to an audio file
    try:
        audio_file = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
    except Exception as e:
        print("Error while converting audio data to audio file:", e) # Debug statement to check if audio data is converted correctly
    # Perform speech recognition
    try:
        text = recognizer.recognize_google(audio_file)
        print("Recognized text: ", text) # Debug statement to check if recognition is done correctly
        return jsonify({"status": "success", "text": text})
    except sr.UnknownValueError as e:
        print("Error while recognizing speech:", e) # Debug statement to check if error occurred while recognizing speech
        return jsonify({"status": "error", "message": "Unable to recognize speech"})
    except sr.RequestError as e:
        print("Error while requesting results from Google Speech Recognition service:", e) # Debug statement to check if error occurred while requesting results
        return jsonify({"status": "error", "message": f"Error while requesting results from Google Speech Recognition service: {e}"})



if __name__ == '__main__':
    app.run()