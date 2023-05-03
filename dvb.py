import json, os
import pyttsx3, vosk, pyaudio, requests

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')
for voice in voices:
    if voice.name == 'Microsoft David Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('model_small')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()


print('start')

data = {}
for text in listen():
    if text == 'close':
        print('close')
        quit()
    elif text == "random" or text == "next":
        req = requests.get('https://www.boredapi.com/api/activity')
        data = req.json()
        print(f'Activity {data["activity"]}')
        speak(data["activity"])
    elif text == 'type':
        if data:
            name = data["type"]
            print(f'Type {data["type"]}')
            speak(data["type"])
    elif text == 'participants':
        if data:
            participants = data["participants"]
            print(f'Participants {data["participants"]}')
            speak(str(data["participants"]))
    elif text == 'save':
        if data:
            with open('result.txt', 'a') as f:
                f.write(json.dumps(data) + '\n')
                speak('recorded')
        else:
            speak('nothing to record')
    else:
        print(text)
