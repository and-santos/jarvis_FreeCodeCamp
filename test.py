import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    print(voice.id, voice.name, voice.languages)

engine.setProperty('voice', 'brazil')
engine.setProperty('rate', 120)
engine.setProperty('volume', 1.)

engine.say('amador')
engine.say('programa')
engine.runAndWait()
