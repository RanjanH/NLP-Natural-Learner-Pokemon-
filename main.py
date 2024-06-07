import speech_recognition as sr
import pyttsx3
import nltk
import sys
import json

r = sr.Recognizer()
semantics = {'switch' : ['come back go','switch with'],'move' : ['use','strike with','attack with']}
cmds = ['switch','come back','use','go']

pokeData = open("data/species.json",'r')
pokemons = json.load(pokeData)
moveData = open("data/moves.json",encoding="utf-8")
moves = json.load(moveData)

def pos_tag(tokens):
    tagged = []
    for i in range(0,len(tokens)):
        if tokens[i].lower() in pokemons:
            tagged.append((tokens[i],'NNP'))
        elif tokens[i].lower() in moves:
            tagged.append((tokens[i],'NNM'))
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

def namedEntityExtractor(tagged):
    pokemon = {1:'',2:''}
    move = ''
    for (name,tag) in tagged:
        if tag == 'NNP':
            if not pokemon[1]:
                pokemon[1] = name
            else:
                pokemon[2] = name
        elif tag == 'NNM':
            move = name

    return pokemon, move

def commandIdentifier(tagged):
    global semantics
    gram = {1:[],2:''}
    cmd = ''
    for (name,tag) in tagged:
        if tag != 'NNP' and tag != 'NNM':
            gram[1].append(name)
    if len(gram[1]) == 2:
        gram[2] += gram[1][0] + ' ' + gram[1][1]
        cmd = gram[2]
    elif len(gram[1]) == 3:
        for i in gram[1]:
            gram[2] += i + ' '
        gram[2] = gram[2].strip()
        cmd = gram[2]
    elif len(gram[1]) != 0:
        cmd = gram[1][0]
    flag = False
    for i in semantics.keys():
        if cmd in semantics[i]:
            flag = True
            print(f"Command - {i}")
            break
    if not flag:
        print('Not a valid command')        


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
                pokemon, move = namedEntityExtractor(tagged)
                print(f"Pokemon - {pokemon}\nMove - {move}")
                commandIdentifier(tagged)
                #gram2 = [token[i] + ' ' + token[i+1] for i in range(0,len(token))]

            except Exception as e:
                print(f"Come again....{e}")

    except sr.RequestError as e:
        print(f"Could not request results : {e}")

    except sr.UnknownValueError:
        print("Unknown Value Error")