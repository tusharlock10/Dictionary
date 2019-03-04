import sys, dictionary

ALL_ARGS=['--ADD', '-A', '--SEARCH', '-S']
args=sys.argv[1:]

if args[-1] in ALL_ARGS:
    arg=args[-1]
else:
    arg='-S'

word=''.join(args.remove(arg))

    
if arg in ['--ADD','-A']:
    dictionary.add_new_word()
else:
    dictionary.search_word(word)