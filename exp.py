from nltk.corpus import wordnet as wn
import nltk, json

#from nltk.corpus import words
#not using words.words() because its bullshit

'''
TYPES={
'CC':'Conjunction', 'CD':'Cardinal Digit', 'DT': 'Determiner', 'EX': 'Existential', 'FW': 'Foreign Word',
'IN' :'Preposition', 'JJ' :'Adjective', 'JJR': 'Bigger Adjective', 'JJS': 'Superlative Adjective',
'LS' :'List Marker', 'MD' :'Modal', 'NN' :'Singular Noun', 'NNS': 'Plural Noun', 'NNP': 'Singular Proper Noun',
'NNPS': 'Plural Proper Noun', 'PDT' :'Pre-determiner', 'POS' :'Possesive', 'PRP' :'Personal Pronoun',
'PRP$': 'Posessive Pronoun', 'RB' :'Adverb', 'RBR': 'Bigger Adverb', 'RBS': 'Superlative Adjective',
'RP': 'Particle', 'TO': 'N/A', 'UH': 'Interjection', 'VB': 'Verb', 'VBD': 'Verb, Past Tense',
'VBG': 'Verb, Present','VBN': 'Verb, Past Participle', 'VBP': 'Verb, Singular Present',
'VBZ': 'Verb, 3rd Person Singular Present', 'WDT': 'WH-determiner', 'WP': 'WH-pronoun', 'WP$': 'Possessive WH-pronoun',
'WRB': 'WH-abverb'
}
'''


L=[]
f=open('words.txt')
data=f.read()
f.close()
L=data.split('\n')


D={}

empty_words=[]


for word in L:
    word=word.upper()
    D_word={}   # {WORD:{'MEANINGS':{...}, 'ANTONYMS':[...], 'SYNONYMS:[...]'}}
    
    #help(S[0])
    #1/0

    ALL_TYPES={'n':'Noun', 'v':'Verb', 'a':'Adjective','s':'Adjective', 'r':'Adverb'}



    MEANINGS={} # 'MEANINGS':{SENSE_NUM_1:[TYPE_1, MEANING, CONTEXT, EXAMPLE], SENSE_NUM_2:[TYPE_2, MEANING, CONTEXT, EXAMPLE]}'
    SYNONYMS = set()
    ANTONYMS = set()
    sense=[]
    S=wn.synsets(word)


    def get_context(syn):
        HYPERNYMS=syn.hypernyms()
        result=[]
        for i in HYPERNYMS:
            temp=i.lemma_names()
            temp=[' '.join(i.capitalize().split('_')) for i in temp]
            result+=temp

        return result


    for syn in S:

        for l in syn.lemmas():
            temp=' '.join(l.name().capitalize().split('_'))
            SYNONYMS.add(temp) 
            if l.antonyms(): 
                ANTONYMS.add(l.antonyms()[0].name()) 

        syn_name=syn.name().split('.')[0].upper()
        if syn_name!=word:continue

        sense_num=int(syn.name().split('.')[-1])
        if sense_num in sense:
            continue

        t=ALL_TYPES[syn.pos()]  # type
        m=syn.definition() # meaning
        c=get_context(syn) # context
        e=syn.examples() # examples

        temp={sense_num:[t, m, c, e]}
        MEANINGS.update(temp)

    try:SYNONYMS.remove(word)
    except:pass
    try:ANTONYMS.remove(word)
    except:pass
    SYNONYMS, ANTONYMS=list(SYNONYMS)[:5], list(ANTONYMS)[:5]
    if MEANINGS!={} or SYNONYMS!=[]:
        D_word={word:{'MEANINGS':MEANINGS,'ANTONYMS':ANTONYMS, 'SYNONYMS':SYNONYMS}}
        D.update(D_word)
    else:
        empty_words+=[word]


L=[chr(ord('A')+i) for i in range(26)]

L=L
for i in L:
    D2={}
    print(i)
    for word in D:
        if word[0].upper()==i:
            D2.update({word: D[word]})

    f=open(f'data\\D{i}.json','w')
    data=json.dumps(D2)
    f.write(data)
    f.close()

f=open('data\\empty_words.txt','w')
f.write('\n'.join(empty_words))
f.close()