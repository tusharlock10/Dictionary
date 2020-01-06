import json, time
import os
from difflib import SequenceMatcher as SM
import tj,sys
from pyunpack import Archive
# import downloader
import urllib.request

FILE='D.json'


cwd=os.path.dirname(__file__)
os.chdir(cwd)

D={}
D_List=[]



def setter():
    dir_name=os.path.dirname(sys.argv[0])
    link=r'https://www.dropbox.com/s/qjdgnf6npiqymgs/data.7z?dl=1'
    data_file=os.path.join(dir_name, 'data.7z')
    print("Data file is: ",data_file)

    # d=downloader.Download(link, data_file)

    try:
        print('Trying to recover the data from data.7z file')
        Archive(data_file).extractall(dir_name)
        print('Data retrival successful, program will now function normally...')
    except:
        print('Data retrival failed as data.7z was not found...')
        print('Trying to download data.7z from internet')
        try:
            # d.download()
            urllib.request.urlretrieve(link, data_file)
            Archive(data_file).extractall(dir_name)
        except:
            print('Could not download the database due to connection issue...')
            print('Restart the program, with a proper internet connection...')
            input('Enter to quit...')
        sys.exit()


def __get_words(word, D_List):
    if word.upper() in D_List:
        return word.upper()
    else:
        Word_List=[i for i in D_List if i[0].upper()==word[0].upper()]
        Matches={}

        for test_word in Word_List:
            ratio=SM(None,test_word.upper(), word.upper()).ratio()
            if ratio>0.72:
                temp={test_word:round(ratio*100,2)}
                Matches.update(temp)

        val=list(Matches.values())
        val.sort(reverse=1)
        val=val[:5]
        temp={}

        for j in val:
            for i in Matches:
                if Matches[i]==j:
                    temp.update({i: j})
        Matches=temp

        if len(Matches)==0:
            word=tj.color_text(word.upper(), text_color='YELLOW',
                                            bold=True, underline=True)
            print(f'\nWord your entered: {word}')
            print(f"{'-'*60}")
            print('No close matches were found, you might have entered a wrong word...')
            return None

        else:
            print(f'{word.upper()} was not found. We found {len(Matches)} close matches:')
            print('+-----------------------------+')
            print('|    Word  -  Percent Match   |')
            print('+-----------------------------+')
            j=0
            for i in Matches:
                j=j+1
                print('| %-16s - %-9s|' % ( i, f'{Matches[i]} %'))
            print('+-----------------------------+')
            best_match=list(Matches.keys())[0]
            print(f'\n**{best_match} ({Matches[best_match]} %) is the best match for the word - {word.upper()}')
        return best_match.upper()

def print_meanings(word,data):
    print('WORD: ',word)
    MEANINGS=data['MEANINGS']
    ANTONYMS=data['ANTONYMS']
    SYNONYMS=data['SYNONYMS']

    if SYNONYMS!=[]:
        SYNONYMS=', '.join(SYNONYMS)
        print('SYNONYMS: ',SYNONYMS)
    if ANTONYMS!=[]:
        ANTONYMS=', '.join(ANTONYMS)
        print('ANTONYMS: ',ANTONYMS)
    print('\n')

    L=[]
    j=0
    print(' -- MEANINGS --\n')
    to_print='\n  NO MEANINGS AVAILABLE FOR THIS WORD'
    for sense_num in MEANINGS:
        template=f'  * %s (%s) - %s\n%s%s'   # word, t, m, c, e
        temp=MEANINGS[sense_num]
        t=temp[0]
        m=temp[1]
        c=temp[2]
        if c!=[]:
            c='\tIN CONTEXT WITH: '+'/ '.join(c)
        else:
            c=''


        e=temp[3]
        e=[f'{str(i)}. {e[i]}' for i in range(len(e))]
        if e!=[]:
            e='\n\tEXAMPLES :-\n\t\t'+'\n\t\t'.join(e)
        else:
            e=''
        L+=[template % (word, t, m, c, e)]
        to_print=f'\n\n'.join(L)
        j+=1
        if j%2==0:
            print(to_print)
            to_print=''
            L=[]
            choice=tj.instant_input().upper()
            if choice=='Q':
                return None
    print(to_print)



def search_word(word):
    global D_List, D

    letter=word[0].upper()

    try:
        f=open(f'data\\D{letter}.json')
        data=f.read()
        D=json.loads(data)
        f.close()
        D_List=D.keys()
    except:
        print('The database is either corrupt or not present...')
        print('Downloading the data from online database (around 3.1 MB)..')
        setter()
        f=open(f'data\\D{letter}.json')
        data=f.read()
        D=json.loads(data)
        f.close()
        D_List=D.keys()


    word=__get_words(word, D_List)
    if word!=None:
        data=D[word]
        print_meanings(word, data)


def add_new_word():
    word=input('Enter the new word: ').upper()
    letter=word[0].upper()

    try:
        f=open(f'data\\D{letter}.json')
        D=f.read()
        D=json.loads(D)
        f.close()
    except:
        print('The database appears to be corrupt...')
        print('Downloading the data from online database (around 3.1 MB)...')
        setter()
        f=open(f'data\\D{letter}.json')
        D=f.read()
        D=json.loads(D)
        f.close()

    ANTONYMS=input('Enter antonyms for this word, seperated by a comma:- \n>>>').split(',')
    ANTONYMS=[i.strip().capitalize() for i in ANTONYMS]

    SYNONYMS=input('Enter synonyms for this word, seperated by a comma:- \n>>>').split(',')
    SYNONYMS=[i.strip().capitalize() for i in SYNONYMS]

    MEANINGS={}
    i=0
    print('YOU CAN PRESS ENTER TO SKIP, AND PRESS Q TO QUIT IN ANY OF THESE FIELDS-')
    while True:
        i+=1
        print('-'*40,'\n')

        m=input(f'Enter the meaning of this word-\nm{i}>>>')
        if m.upper()=='Q':break
        t=input(f'Enter the type of this word (Noun/ Verb/ Adverb, etc...)-\nt{i}>>>').capitalize()
        if t.upper()=='Q':break
        c=input(f'Enter the context of this meaning, seperated by / (Action/ Person/ Material etc...)-\nc{i}>>>')
        if c.upper()=='Q':break
        elif c=='':c=[]
        else:c=c.split('/')
        e=input(f'Enter an example to understand well, for multiple examples, add | to seperate examples-\ne{i}>>>')
        if e.upper()=='Q':break
        elif e=='':e=[]
        else:e=e.split('|')

        temp={i:[t,m,c,e]}
        MEANINGS.update(temp)

    D_word={word:{'MEANINGS':MEANINGS,'ANTONYMS':ANTONYMS, 'SYNONYMS':SYNONYMS}}
    D.update(D_word)

    f=open(f'data\\D{letter}.json','w')
    D=json.dumps(D)
    f.write(D)
    f.close()

    print('Word added successfully...')

    return word