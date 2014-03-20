termCube v0.1.1-alpha
========

A terminal-based NxNxN cube game (curses speedsolving/speedcubing).

For specific technical goals see GOALS.

*NOTE: This is an in-progress, hobby project with flexible goals/end-dates.*

Purpose
========

To enjoy speed-cubing via a fast, clean, simple, terminal-based-GUI game.

And personally for a lurning experience, in order to:

  1. Learn git (commands, website, explore other projects, collaboration, etc) 
  2. Explore python curses (fast screen printing, mouse control, keyboard input, and windows) 
  3. Better own python project management
  4. Use numpy for matrix manipulation
  5. Attack a problem many have so easily tackled before, but in a (probably) slower, uglier, and dirtier way

Version
========

See title above in format: MAJOR.MINOR.BUILD[-PRE[+META]]. Pretty much in alpha/beta we'll mostly update MINOR/BUILD when we think of it.

This is [Semantic Versioning](http://semver.org/) v2.0.0. Everything else you can get through Git history.

Elements
========

  * demo/curses*: Learning curses..NOT a demo of termCube capability!

Dependencies (& Thanks!)
========

Required Python non-builtin modules
--------
  * [argparse, via PyPi](https://pypi.python.org/pypi/argparse) -- command line arguments, easy to install
    * ONLY if your `$ env python --version` is < 2.7.x
    * Python License, Copyright (c) 1990-2013 [Python Software Foundation](https://www.python.org/psf)

Optional Python non-builtin modules
--------
  * [PuDB](https://github.com/inducer/pudb) -- Neat python graphical debugger
    * [MIT](http://opensource.org/licenses/MIT) License, Copyright (c) 2009-2013 Andreas Kloeckner, LA: 18-Mar-2014

Optional linux program
--------
  * xterm -- terminal emulator for X

Inspiration (& Thanks!)
========

  * [term2048](https://github.com/bfontaine/term2048) for its simplicity and funicity

License
========

[MIT](http://opensource.org/licenses/MIT) License, Copyright (c) 2014 Originally by [IDrmHyprbls](https://github.com/idrmhyprbls), see COPYRIGHT file for all contributors

