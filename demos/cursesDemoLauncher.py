#!/usr/bin/env python
"""Python launcher for cursesDemo.py.

Used to catch syntax errors if raised in the demo when called by the XTerm 
cursesDemoLauncher bash script, the new XTerm won't simply close (from +hold) 
due to the compile time error, but instead will print it on stderr.

"""

from __future__ import print_function
import sys
from subprocess import call
from time import sleep
#from pudb import set_trace; set_trace()  # To step though whole program

if __name__ == '__main__':
    ARGS = sys.argv[1:]
    try:
        from cursesDemo import _main
        _main(ARGS)
    except SyntaxError as e:
        print(__file__ + ": Syntax error: \"%s\" (%s)" % (str(e), e.__doc__), file=sys.stderr)
        print(__file__ + ": Exiting...", file=sys.stderr)
        if 'xterm' in ARGS:
            sleep(3)

