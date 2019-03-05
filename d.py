import sys, dictionary,os

dir_name=os.path.dirname(sys.argv[0])
paths=os.environ['PATH']

if dir_name not in paths:
    os.environ['PATH']+=os.pathsep+dir_name


logo=''' * WELCOME TO *

-------------------------------+
    ____  _      __  _         |                    
   / __ \(_)____/ /_(_)___  ___|  ____ ________  __
  / / / / / ___/ __/ / __ \/ __ \/ __ `/ ___/ / / /
 / /_/ / / /__/ /_/ / /_/ / / / / /_/ / /  / /_/ / 
/_____/_/\___/\__/_/\____/_/ /_/\____/_/   \____/  
                               |          /____/   
                               |
-------------------------------+
        - TJ Productions 2019'''


main_menu=rf'''

{logo}


 MAIN MENU-

 1) Search a word
 2) Add a new word in Database
 3) Read the docs
 4) Quit


'''

__doc__=r'''

 * D I C T I O N A R Y * 

A command-line program that lets you search meanings of words 
in a jiffy, just from your command-line, and that too offline.

 -> DICTIONARY is probably the most advanced command-line english.

 DICTINARY uses an a custom-made database, derived from NLTK library
 in Python. In short, the DICTIONARY database is reliable and full of 
 information.

 You type the word and dictionary will provide you all the information 
 that it has, regarding that word!

The usage of this program is also very easy.

You can use the program in 2 ways. First is to directly open the program
and run it. Second is a faster way, to do your tasks without even having
to open the program. 

First way-
Just run the program and follow on-screen instructions.

Second way-
Use command-line arguments. Its is the faster way for doing things.

    How to use this method-
    a. Make sure this program is in your environment variables
        (although the program takes care of this, but still, if you
        are unale to operate this program from command-line, you know
        what to do)
    b. Use this program using arguments such as -S, -A, -H, -D

    c. -S is used for searching a word in dictionary. To use it, 
    just write 'd <your word> -s' and the program will show you the
    information regarding that word. Also, even if you don't provide this
    -S, argument, still the program will function in the same way as -S
    is the default argument.

    d. -A to add a new word. 'd -A' and this command will let you add a
    new word in your dictionary.

    e. -D/ -H for help. If you need help regarding how to use this program,
    you can use the 'd -D' or 'd -H' command.
 
'''

def main():
    msg='Enter your choice from 1-4: '
    while True:
        os.system('cls')

        print(main_menu)

        choice = input(msg)
        if choice =='1':
            print('\n\n ** STARTING SEARCH **')
            word=input('\nEnter a word: ')
            dictionary.search_word(word)
            input('Enter to continue...')

        if choice =='2':
            print('\n\n ** ADDING NEW WORD **')
            dictionary.add_new_word()
            input('Enter to continue...')

        if choice == '3':
            print('\n\n ** GETTING THE DOCS READY **')
            print(__doc__)
            input('Enter to continue...')

        if choice =='4':
            print('\n\n  ** GOODBYE **')
            break

        if choice not in ['1', '2','3','4','5']:
            msg='Enter only numbers from 1 to 4: '
        else:
            msg='Enter your choice: '




ALL_ARGS=['--ADD', '-A', '--SEARCH', '-S','-D','--DOC', '-H','--HELP']
args=sys.argv[1:]
args=[i.upper() for i in args]

if args==[]:
    arg='MAIN'

elif args[-1] in ALL_ARGS:
    arg=args[-1]
else:
    arg='-S'



    
if arg in ['--ADD','-A']:
    dictionary.add_new_word()


elif arg=='MAIN':
    main()
    sys.exit()

elif arg in ['-D','--DOC','-H','--HELP']:
    os.system('cls')
    print(__doc__)

elif arg in ['-S','--SEARCH'] :
    try:word=''.join(args.remove(arg))
    except:word=''.join(args)
    dictionary.search_word(word)