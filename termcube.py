#!/usr/bin/env python
"""

                              Term Cube
   Time: 00:00:00.000 +-------+-------+-------+ +-----+-----+-----+
   Date: 00-00-00     |       |       |       | |     |     |     |
   User: XXX          |       |       |       | |     |     |     |
    Pts: XXX          +-------+-------+-------+ +-----+-----+-----+
    Tty: XXX          |       |   U   |       | |     |  B  |     |
   Host: XXX          |       |       |       | |     |     |     |
     OS: XXX          +-------+-------+-------+ +-----+-----+-----+
   Disp: XXX          |       |       |       | |     |     |     |
  PyVer: XXX          |       |       |       | |     |     |     |
  TCVer: XXX          +-------+-------+-------+ +-----+-----+-----+
  +-----+-----+-----+ +-------+-------+-------+ +-----+-----+-----+
  |     |     |     | |       |       |       | |     |     |     |
  |     |     |     | |       |       |       | |     |     |     |
  |     |     |     | |       |       |       | |     |     |     |
  +-----+-----+-----+ +-------+-------+-------+ +-----+-----+-----+
  |     |     |     | |       |       |       | |     |     |     |
  |     |  L  |     | |       |   F   |       | |     |  R  |     |
  |     |     |     | |       |       |       | |     |     |     |
  +-----+-----+-----+ +-------+-------+-------+ +-----+-----+-----+
  |     |     |     | |       |       |       | |     |     |     |
  |     |     |     | |       |       |       | |     |     |     |
  |     |     |     | |       |       |       | |     |     |     |
  +-----+-----+-----+ +-------+-------+-------+ +-----+-----+-----+
   F  : ?   U  : ?    +-------+-------+-------+  Time: 00:00:00.000 
   F' : ?   U' : ?    |       |       |       | TBest: 00:00:00.000
   F" : ?   U" : ?    |       |       |       | TLast: 00:00:00.000
   F2 : ?   U2 : ?    +-------+-------+-------+  TAvg: 00:00:00.000
   F2': ?   U2': ?    |       |       |       |  Move: 000
   F2": ?   U2": ?    |       |   D   |       | MBest: 000
   L  : ?   D  : ?    +-------+-------+-------+ MLast: 000
   L' : ?   D' : ?    |       |       |       |  MAvg: 000
   L" : ?   D" : ?    |       |       |       | Sec/M: 000.000
   L2 : ?   D2 : ?    +-------+-------+-------+ Reset: 000
   L2': ?   D2': ?       Seed: 000000000000      Wins: 000
   L2": ?   D2": ?                               Loss: 000                  
   R  : ?   B  : ?                                Tot: 000
   R' : ?   B' : ?                             
   R" : ?   B" : ? 
   R2 : ?   B2 : ?    
   R2': ?   B2': ?    
   R2": ?   B2": ?    
   Q  : ^C  R  : ^D

http://docs.python.org/2/howto/curses.html#curses-howto

"""

from __future__ import print_function, division
from random import randint
from string import digits, letters
from time import time, sleep
import curses

def mainloop(window):
    ymax, xmax = window.getmaxyx()
    pass

def noise(window):
    mid, mx, my, mz, mbstate = 0, 0, 0, 0, 0
    ymax, xmax = window.getmaxyx()
    window.timeout(0)  # Nonblocking gets, 0 in ms
    t0 = time()
    tot = 0
    window.addch(ymax-7, 24, curses.ACS_LARROW)
    window.hline(ymax-7, 25, curses.ACS_HLINE, 10)
    window.addstr(ymax-7, 36, "click this box, or press h, or q")
    win2 = curses.newwin(12, 21, ymax-13, 1)
    win2.box()
    win2.keypad(1)
    win2.nodelay(1)
    win2.border()
    win2.leaveok(0)
    win2.scrollok(0)
    win2.bkgd(' ', 0)
    win2_inv = False
    while True:
        t1 = time()
        tot += 1
        ups = tot/(t1-t0)
        x = randint(1, randint(1, xmax - 2))
        y = randint(1, randint(1, ymax - 2 - 12))
        c = ord('#')
        getch = window.getch() 
        if getch == curses.KEY_MOUSE or getch == ord('h'):
            tmid, tmx, tmy, tmz, tmbstate = curses.getmouse()
            if getch == ord('h') or tmbstate == 2 and win2.enclose(tmy, tmx):
                mid, mx, my, mz, mbstate = tmid, tmx, tmy, tmz, tmbstate
                if win2_inv:
                    win2.attroff(curses.A_REVERSE)
                else:
                    win2.attron(curses.A_REVERSE)
                win2_inv = not win2_inv
        elif getch == ord('q'):
            raise SystemExit(None)
        window.addch(y, x, c)
        window.noutrefresh()  # Mark for update

        ylst, xlst = curses.getsyx()
        win2.addstr(12-11, 1, "tot   :%12i" % tot)
        win2.addstr(12-10, 1, "#/s   :%12.3f" % ups)
        win2.addstr(12-9,  1,  "t tot :%12.3f" % (t1-t0))
        win2.addstr(12-8,  1,  "y lst :%12i" % ylst)
        win2.addstr(12-7,  1,  "x lst :%12i" % xlst)
        win2.addstr(12-6,  1,  "m id  :%12i" % mid)
        win2.addstr(12-5,  1,  "m x   :%12i" % mx)
        win2.addstr(12-4,  1,  "m y   :%12i" % my)
        win2.addstr(12-3,  1,  "m z   :%12i" % mz)
        win2.addstr(12-2,  1,  "m st  :%12i" % mbstate)
        win2.noutrefresh()

        #sleep(1/100000.)
        curses.doupdate()  # Perform refreshes
        continue

def entry(window):
    window.addstr(0, 0, "Type anything and I shall reverse its color: ")
    curses.echo()
    #window.setyx(1, 0)
    istr = window.getstr()
    window.addstr(1, 0, str(istr), curses.A_REVERSE)
    window.refresh()
    curses.noecho()

    try:
        pad = curses.newpad(10, 10)
        pad.addch(0, 0, 'x')
        pad.addch(1, 0, 'x')
        pad.addch(0, 1, 'x')
        pad.addch(1, 1, 'x')
        pad.addch(8, 8, 'x')
        pad.addch(8, 9, 'x')
        pad.addch(9, 8, 'x')
        try:
            pad.addch(9, 9, 'x')
        except curses.error as e:
            window.move(0, 0)
            pass
        pad.refresh(0, 0, 0, 0, 11, 11)
        #pad.addch(99, 99, 'x')
        #for y in range(0, 100):
        #    for x in range(0, 100):
        #        try:
        #            v = ord('a') + (x*x+y*y) % 26
        #            pad.addch(y, x, v)
        #        except curses.error as e:
        #            pass
        ## Displays a section of the pad in the middle of the window
        #pad.refresh(0,0, 5,5, 20,75)
    except Exception as e:
        raise
    sleep(2)

def _main():
    try:
        window = curses.initscr()       # Window object
        window.clear()                  # Erase and repaint on update
        curses.setupterm("NAME")        # Setup term name and file out
        availmask, oldmask = \
                curses.mousemask(curses.BUTTON1_PRESSED | 
                                 curses.BUTTON1_RELEASED)  # Record mouse events
        curses.mouseinterval(1)         # Max ms click interval
        curses.start_color()            # To use colors
        curses.use_default_colors()     # Default term colors eg transparency
        curses.meta(1)                  # 8b characters
        curses.noecho()                 # No auto echo keys to window
        curses.cbreak()                 # Don't wait for <Enter>
        window.keypad(1)                # Use special char values
        window.nodelay(1)               # Nonblocking getch/getstr
        window.border()                 # Or box on edges
        window.leaveok(0)               # Virtual screen cursor after update
        curses.curs_set(0)              # Invisible curser
        window.scrollok(0)              # Cursor moves off page don't scroll
        window.bkgd(' ', 0)             # Set background char and attr
        #example(window)
        noise(window)
        #pad()
    finally:
        curses.nocbreak()
        window.keypad(0)
        curses.echo()
        curses.endwin()
    #mainloop()

if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        pass
    except curses.error as e:
        #print("ERROR: Check window size!")
        raise
    except Exception as e:
        raise
    except:
        raise
    #raise SystemExit(None)

