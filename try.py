import nltk

sentence = input("Enter a string : ")
pokemons = ['pikachu','caterpie','pidgey','bulbasaur','charmander']
cmds = ['switch','come back','use','go']
token = nltk.word_tokenize(sentence)
print('Tokens = ',token)

def pos_tag(tokens):
    tagged = []
    for i in range(0,len(tokens)):
        if tokens[i].lower() in pokemons:
            print(tokens[i])
            tagged.append((tokens[i],'NNP'))
        elif tokens[i] in cmds:
            if i != 0:
                if tokens[i-1].lower() in pokemons or tokens[i+1].lower() in pokemons:
                    print(tokens[i])
                    tagged.append((tokens[i],'VB'))
            else:
                if tokens[i+1].lower() in pokemons:
                    tagged.append((tokens[i],'VB'))
        else:
            tag = nltk.pos_tag([tokens[i]])
            for i in tag:
                tagged.append(i)
    return tagged

tagged = pos_tag(token)
print(tagged)

#print(nltk.chunk.ne_chunk(tagged))