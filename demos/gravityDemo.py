#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Warning: External bug - if the term window is > 220 in width (x),
#          mouse events will bomb

from __future__ import print_function, division
import curses
import os

# os.environ['TERM']='xterm-1002'  # To use mouse-hold
os.environ['TERM']='xterm-256color'
COLOR_RED = 1
COLOR_BLUE = 2

def addch(win, y, x, ch, *args):
    try:
        win.addch(y, x, ch, *args)
    except:
        pass

def init_win(win):
    ymax, xmax = win.getmaxyx()
    win.clear()
    # win.border()  # Or box on edges
    # addch(win, 0, 0, '+')
    # addch(win, 0, xmax-1, '+')
    # addch(win, ymax-1, 0, '+')
    # try:
    #     addch(win, ymax-1, xmax-1, '+')
    # except:
    #     win.move(0, 0)
    win.noutrefresh()  # Mark for update

def init_screen():
    screen = curses.initscr()  # Window object
    screen.clear()  # Erase and repaint on update
    availmask, oldmask = curses.mousemask(
            curses.BUTTON1_PRESSED | curses.BUTTON1_RELEASED | \
                    curses.BUTTON1_DOUBLE_CLICKED)  # Record mouse evnts
    curses.mouseinterval(0)  # Max ms click interval
    curses.start_color()  # To use colors
    curses.use_default_colors()  # Default term colors eg transparency
    curses.init_pair(COLOR_RED, curses.COLOR_RED, -1)
    curses.init_pair(COLOR_BLUE, curses.COLOR_BLUE, -1)
    curses.meta(1)  # 8b characters
    curses.noecho()  # No auto echo keys to window
    curses.cbreak()  # Don't wait for <Enter>
    screen.keypad(1)  # Use special char values
    screen.nodelay(1)  # Nonblocking getch/getstr
    screen.timeout(1)  # Nonblocking gets, 0 in ms
    screen.leaveok(0)  # Virtual screen cursor after update
    curses.curs_set(0)  # Invisible curser
    screen.scrollok(0)  # Cursor moves off page don't scroll
    return screen

def create_win(screen):
    ymax, xmax = screen.getmaxyx()
    if xmax > 220:
        xmax = 220
    screen.bkgd(' ', 0)  # Set background char and attr
    screen.clear()
    win = screen.subwin(ymax, xmax, 0, 0)
    init_win(win)
    return win

def release_screen(screen):
    screen.move(0, 0)
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

class Entity(object):
    def __init__(self, y_orig, x_orig):
        self.y_pos = 1.
        self.x_pos = 1.
        self.y_last = 1.
        self.x_last = 1.
        self.y_orig = y_orig
        self.x_orig = x_orig

    def setpos(self, y, x):
        if y is not None:
            self.y_pos = y
            self.y_last = y
        if x is not None:
            self.x_pos = x
            self.x_last = x

    @property
    def x(self):
        return int(self.x_pos)
    @x.setter
    def x(self, val):
        self.setpos(None, val)

    @property
    def y(self):
        return int(self.y_pos)
    @y.setter
    def y(self, val):
        self.setpos(val, None)

    def update(self):
        self.setpos(self.y_pos + 1., self.x_pos + 1.)

def main():
    try:
        # Create screen
        screen = init_screen()

        # Create window
        win = create_win(screen)
        ymax, xmax = win.getmaxyx()
        y_orig, x_orig = ymax//2, xmax//2

        # Refresh window
        curses.doupdate()  # Perform refreshes

        # Create character
        comet = Entity(y_orig, x_orig)

        # Update loop
        while True:
            getch = screen.getch() 
            if getch == curses.KEY_MOUSE:
                devid, x, y, z, bstate = curses.getmouse()
                if bstate == 2 and y > 0 and y < ymax-1 and x > 0 and x < xmax-1:
                    addch(win, comet.y, comet.x, ' ')
                    comet.setpos(y, x)
                    addch(win, comet.y, comet.x, '#', curses.color_pair(
                        COLOR_RED))
                    win.addstr(ymax-1, xmax-19, ' y, x = {:3d}, {:3d} '.\
                            format(comet.y, comet.x))
                    win.noutrefresh()  # Mark for update
            addch(win, comet.y, comet.x, ' ')
            comet.update()
            addch(win, comet.y, comet.x, '#', curses.color_pair(
                COLOR_RED))
            win.noutrefresh()  # Mark for update

            # Refresh
            curses.doupdate()

            # Sleep
            curses.napms(50)

    except KeyboardInterrupt:
        pass

    finally:
        release_screen(screen)
        print(comet.y, comet.x)

if __name__ == '__main__':
    main()

