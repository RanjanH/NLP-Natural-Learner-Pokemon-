import speech_recognition as sr
import pyttsx3
import nltk
import sys
import json

r = sr.Recognizer()
semantics = {'switch' : ['come back','switch','go','take care'],'move' : ['use']}
cmds = ['switch','come back','use','go']

pokeData = open("data/species.json",'r')
pokemons = json.load(pokeData)
moveData = open("data/moves.json",encoding="utf-8")
moves = json.load(moveData)

def pos_tag(tokens):
    tagged = []
    for i in range(0,len(tokens)):
        if tokens[i].lower() in pokemons or tokens[i].lower() in moves:
            tagged.append((tokens[i],'NNP'))
        elif tokens[i] in cmds:
            if i != 0:
                if tokens[i-1].lower() in pokemons or tokens[i+1].lower() in pokemons:
                    tagged.append((tokens[i],'VB'))
            else:
                if tokens[i+1].lower() in pokemons:
                    tagged.append((tokens[i],'VB'))
        else:
            tag = nltk.pos_tag([tokens[i]])
            for i in tag:
                tagged.append(i)
    return tagged

def grams(text):
    gram = {1:[],2:[]}
    for i in text:
        pass

with sr.Microphone() as source:
    try:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 0.5
        print("Started Listening.....")
        while True:
            audio = r.listen(source)
            print(f"Recognizing the audio")
            try:
                cmd = r.recognize_google(audio,language = "en")
                if cmd == 'exit':
                    print("*"*20+"\n"+"Exiting the Program"+"\n"+"*"*20)
                    sys.exit()
                print(f"Did you say : {cmd}")
                token = nltk.word_tokenize(cmd)
                tagged = pos_tag(token)
                print(tagged)
                #gram2 = [token[i] + ' ' + token[i+1] for i in range(0,len(token))]

            except Exception as e:
                print(f"Come again....{e}")

    except sr.RequestError as e:
        print(f"Could not request results : {e}")

    except sr.UnknownValueError:
        print("Unknown Value Error")