import speech_recognition as sr
import os 

r = sr.Recognizer()

audio_file = "./wav_voice/output.wav"

with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

try:
    text = r.recognize_google(audio, language="ja-Jp")
    print(text, "recognize OK!")
    

except sr.UnknownValueError:
    print("unknown")
except sr.RequestError as e:
    print("request")

os.remove("./wav_voice/output.wav")