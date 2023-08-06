import argparse
import sys
from notify import notify

def cli(*args, **kwargs):
    example_text = '''examples:
	
	notify 5555555555 "Hello World"

	echo "Hello World" | notify 5555555555,team@popcornnotify.com -s "An Informative Subject Line"

	./script.sh && echo "Script done at $(date)" | notify 555...,team@popcornnotify.com
	'''

    parser = argparse.ArgumentParser(
		prog='notify',
		description='Send simple emails and text messages from one API', 
		epilog=example_text,
		formatter_class=argparse.RawDescriptionHelpFormatter)

    # parser = argparse.ArgumentParser()
    parser.add_argument('recipients', help='Phone numbers or emails to notify, comma separated')
    parser.add_argument('message', help='Message to send', nargs='?')
    parser.add_argument('-s', '--subject', help='Email subject line')
    parser.add_argument('-k', '--api-key', help='By default read from environment variable $POPCORNNOTIFY_API_KEY')
    parser.add_argument('-q', '--quiet', help='Hide all output', action='store_true')

    args = parser.parse_args()
    if args.message:
        # string = open(args.filename).read()
        p_message = args.message
    elif not sys.stdin.isatty():
        p_message = sys.stdin.read()
    else:
        parser.error("too few arguments")

    verbose = True
    if args.quiet:
        verbose = False
    
    notify(recipients=args.recipients, message=p_message, subject=args.subject, api_key=args.api_key, verbose=verbose)
