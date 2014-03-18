#!/usr/bin/env python
"""Curses demo. Not meant to be clean, rather exploratory."""

from       __future__ import print_function, division
from       random     import randint
from       string     import digits, letters, uppercase
from       time       import time, sleep
from       sys        import stderr, argv
from       traceback  import print_exc
import     curses
try:
    from   pudb       import set_trace  # See README
except ImportError:
    from   pdb        import set_trace

MIN_SLEEP = 1/1000000.

def example(window):
    t0 = time()
    tot = 0
    mid, mx, my, mz, mbstate = 0, 0, 0, 0, 0
    ymax, xmax = window.getmaxyx()
    window.timeout(0)  # Nonblocking gets, 0 in ms
    try:
        window.addch(ymax-7, 24, curses.ACS_LARROW)
    except:
        window.move(0, 0)
    window.hline(ymax-7, 25, curses.ACS_HLINE, 10)
    window.addstr(ymax-7, 36, "click this box, type, or press H, or Q")

    # Window 2
    win2 = curses.newwin(12, 21, ymax-13, 1)
    win2.bkgd(' ', curses.A_BOLD | curses.A_REVERSE)
    win2_inv = True
    win2.box()
    win2.keypad(1)
    win2.nodelay(1)
    win2.border()
    win2.leaveok(0)
    win2.scrollok(0)

    # Window 3
    win3 = curses.newwin(3, 21, ymax-6, 36)
    win3.bkgd(' ', curses.A_BOLD)
    win3.box()
    win3.keypad(1)
    win3.nodelay(1)
    win3.border()
    win3.leaveok(0)
    win3.scrollok(0)
    win3_s = ''

    # Mainloop
    while True:
        t1 = time()
        tot += 1
        ups = tot/(t1-t0)
        x = randint(1, randint(1, xmax - 2))
        y = randint(1, randint(1, ymax - 2 - 12))
        c = ord('#')

        # Input
        getch = window.getch() 
        if getch == curses.KEY_MOUSE or getch == ord('H'):
            tmid, tmx, tmy, tmz, tmbstate = curses.getmouse()
            if getch == ord('H') or tmbstate == 2 and win2.enclose(tmy, tmx):
                mid, mx, my, mz, mbstate = tmid, tmx, tmy, tmz, tmbstate
                if win2_inv:
                    win2.bkgdset(' ', curses.A_BOLD)
                else:
                    win2.bkgdset(' ', curses.A_BOLD | curses.A_REVERSE)
                win2_inv = not win2_inv
        elif getch == ord('Q'):
            raise SystemExit(None)

        # Window 1
        try:
            window.addch(y, x, c)  # Totally unbuffered print
        except:
            window.move(0, 0)
        window.noutrefresh()  # Mark for update

        # Window 2
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

        # Window 3
        ylst, xlst = curses.getsyx()
        if getch >= 0x20 and getch < 0x7f and chr(getch) not in uppercase:
            try:
                win3_s += chr(getch)
                win3.addstr(1, 1, win3_s)
                if len(win3_s) > 18:
                    raise curses.error('String too long')
            except:
                win3_s = chr(getch)
                win3.move(0, 0)
        win3.noutrefresh()

        sleep(MIN_SLEEP)
        curses.doupdate()  # Perform refreshes

def main():
    try:
        window = curses.initscr()       # Window object
        window.clear()                  # Erase and repaint on update
        availmask, oldmask = \
                curses.mousemask(curses.BUTTON1_PRESSED | 
                                 curses.BUTTON1_RELEASED)  # Record mouse evnts
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
        example(window)
    finally:
        window.move(0, 0)
        curses.nocbreak()
        window.keypad(0)
        curses.echo()
        curses.endwin()

def _main(args):
    try:
        main()
    except SystemExit as e:
        if not e or str(e).lower() == 'none':
            pass
        else:
            print_exc()
            print('\n' + __file__ + ": SystemExit code \"%s\"" % str(e), 
                    file=stderr)
            curses.napms(3000)
            print('', file=stderr)
    except KeyboardInterrupt:
        pass
    except curses.error as e:
        print_exc()
        print('\n' + __file__ + ": Curses error \"%s\"" % str(e), 
                file=stderr)
        print(__file__ + ": Note: Min window size is 165x45!", file=stderr)
        curses.napms(3000) # Sleep doesn't work here after a curses crash, even with a flush
        print('', file=stderr)
    except Exception as e:
        print_exc()
        print('\n' + __file__ + ": Exception with \"%s\" (%s)" % \
                (str(e), e.__doc__), file=stderr)
        curses.napms(3000)
        print('', file=stderr)
    else:
        pass
    finally:
        print(__file__ + ": Exiting...", file=stderr)
        curses.napms(750)
        raise SystemExit(None)

if __name__ == '__main__':
    _main(argv[1:])

