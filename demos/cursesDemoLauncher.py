#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python launcher for cursesDemo.py.

Note
--------

Used to catch syntax errors if raised in the demo when called by the XTerm 
cursesDemoLauncher bash script, the new XTerm won't simply close (from +hold) 
due to the compile time error, but instead will print it on stderr.

Contents
--------

_Imports_ 
_Metadata_
_Globals_         
_Execution_       

Usage
--------

/termCube/demos $ ./cursesDemoLauncher  # Using XTerm launcher
/termCube/demos $ python -m cursesDemoLauncher  # Using python launcher

"""

########################_Imports_##############################################
#
from   __future__  import print_function
import sys
import os
from   subprocess  import call
from   time        import sleep

#from  pudb import set_trace;    set_trace()  # To step though whole program

from   cursesDemo  import _main_exc_handler

########################_Metadata_#############################################
#
__creator__   = "IDrmHyprbls"
__project__   = "https://github.com/idrmhyprbls/termCube"
__author__    = "https://github.com/idrmhyprbls/termCube/blob/master/COPYRIGHT.md"
__copyright__ = __author__
__license__   = "https://github.com/idrmhyprbls/termCube/blob/master/LICENSE.md"
__version__   = "See <%s>." % __project__

########################_Globals_##############################################
#
ARGS = sys.argv[1:]

########################_Execution_############################################
#
if __name__ == '__main__':
    try:
        _main_exc_handler(ARGS)
    except SyntaxError as e:
        print(__file__ + ": Syntax error: \"%s\" (%s)" % (str(e), e.__doc__), file=sys.stderr)
        print(__file__ + ": Exiting...", file=sys.stderr)
        if 'xterm' in ARGS:
            sleep(3)

