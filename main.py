import speech_recognition as sr
import pyttsx3
import nltk
import sys

r = sr.Recognizer()
semantics = {'switch' : ['come back','switch','go','take care'],'move' : ['use']}

with sr.Microphone() as source:
    try:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 0.5
        print("Started Listening.....")
        while True:
            audio = r.listen(source)
            print(f"Recognizing the audio")
            try:
                cmd = r.recognize_google(audio,language = "en-in")
                if cmd == 'exit':
                    sys.exit()
                print(f"Did you say : {cmd}")
                token = nltk.word_tokenize(cmd)
                tagged = nltk.pos_tag(token)
                print(tagged)
                #gram2 = [token[i] + ' ' + token[i+1] for i in range(0,len(token))]

            except Exception as e:
                print(f"Come again....{e}")

    except sr.RequestError as e:
        print(f"Could not request results : {e}")

    except sr.UnknownValueError:
        print("Unknown Value Error")