import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

def speak(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        os.system(f"mpg123 {fp.name}")  # Install mpg123 on Linux

def listen(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source, timeout=timeout)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand."
    except sr.RequestError:
        return "API error."

def run_interaction(question, resume_data, generate_followup_question_fn):
    speak(question)
    answer = listen()
    print(f"Candidate Answer: {answer}")

    followup = generate_followup_question_fn(question, answer)
    if "✅" in followup:
        print(followup)
        return None
    else:
        return followup
