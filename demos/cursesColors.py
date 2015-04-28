import string
import curses
try:
    import _curses
except ImportError:
    _curses = curses
# import os
# import os.path
# import posixpath
# import string
# import sys
import time
# import traceback
# import glob
# import json
# import string
# import math
# import re
# from subprocess import Popen

# sys.path.append('/usr/local/lib')

NONBLOCKING = True
NONBLOCKING_TIMEOUT = 5  # ms
PRINTABLE = string.printable
ORDINAL = range(32, 127)  # ' ' to '~'

def dlookup_eq(d, l):
    """Return key from a dict if l == val."""
    for k,v in d.iteritems():
        if l == v:
            return k
    return None

def dlookup_in(d, l):
    """Return key from a dict if l in val."""
    for k,v in d.iteritems():
        try:
            if l in v:
                return k
        except TypeError:
            continue
    return None

# special input keys
SKEYS = {
    'NULL': (0,),
    'ESC': (27,24,16),
    'BELL': (7,),
    'HOME': (curses.KEY_HOME,1,2),
    'END': (curses.KEY_END,3,4,23),
    'ENTER': (curses.KEY_ENTER,6,10,12,13),
    'BACKSPACE': (curses.KEY_BACKSPACE,8),
    'TAB': (9,),
    'SHIFTOUT': (curses.KEY_SEND,14),
    'SHIFTIN': (curses.KEY_SBEG,15),
    'INSERT': (curses.KEY_IC,26),
    'DELETE': (curses.KEY_DC,127),
    'PGUP': (curses.KEY_PPAGE,),
    'PGDN': (curses.KEY_NPAGE,),
    'RESIZE': (curses.KEY_RESIZE,),
    'MOUSE': (curses.KEY_MOUSE,),
    'UP': (curses.KEY_UP,),
    'DOWN': (curses.KEY_DOWN,),
    'LEFT': (curses.KEY_LEFT,),
    'RIGHT': (curses.KEY_RIGHT,),
    'F1': (curses.KEY_F1,),
    'F2': (curses.KEY_F2,),
    'F3': (curses.KEY_F3,),
    'F4': (curses.KEY_F4,),
    'F5': (curses.KEY_F5,),
    'F6': (curses.KEY_F6,),
    'F7': (curses.KEY_F7,),
    'F8': (curses.KEY_F8,),
    'F9': (curses.KEY_F9,),
    'F10': (curses.KEY_F10,),
    'F11': (curses.KEY_F11,),
    'F12': (curses.KEY_F12,)}

# left mouse click events
SGL_CLICKS = (curses.BUTTON1_CLICKED, curses.BUTTON1_RELEASED)
DBL_CLICKS = (curses.BUTTON1_DOUBLE_CLICKED, curses.BUTTON1_TRIPLE_CLICKED)

# special input key groups
SKGROUPS = {
    'ARROW': SKEYS['UP'] + SKEYS['DOWN'] + SKEYS['LEFT'] + SKEYS['RIGHT'],
    'FN': SKEYS['F1'] + SKEYS['F2'] + SKEYS['F3'] + SKEYS['F4'] +
          SKEYS['F5'] + SKEYS['F6'] + SKEYS['F7'] + SKEYS['F8'] +
          SKEYS['F9'] + SKEYS['F10'] + SKEYS['F11'] + SKEYS['F12'],
    'KEYPAD': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+',
               '*', '/','.') + SKEYS['ENTER']}

# text colors
CLRS = {  
    # 16 colors can be active at once
    'default': -0x01,
    'red': 0x01,
    # 'magenta': 0x0d,
    # 'dpink': 0xc8,
    'pink': 0xd5,
    # 'dorange': 0xc4,
    'orange': 0xca,
    'brown': 0x5e,
    'yellow': 0xe2,
    'cream': 0xe5,
    'green': 0x02,
    # 'sage': 0x41,
    'lime': 0x52,
    'blue': 0x15,
    # 'navy': 0x13,
    'cyan': 0x0e,
    # 'sky': 0x9f,
    'violet': 0x81,
    # 'indigo': 0x36,
    'white': 0xe7,
    # 'dgray': 0x00,
    'gray': 0xf1,
    'lgray': 0xfa,
    'black': 0x10}

# text attributes
ATTRS = {
         'bold': curses.A_BOLD,
         'dim': curses.A_DIM, 
         'invis': curses.A_INVIS, 
         'norm': curses.A_NORMAL, 
         'rev': curses.A_REVERSE, 
         'uline': curses.A_UNDERLINE}

# color pair attributes created from clrs with access via pairs[(fg,bg)]
pairs = {}

def demo_0(win):
    """Get input key, display input char or int."""
    try:
        inp = ' '
        while 1:
            win.erase()
            win.box()
            win.bkgd(' ', pairs[('white','blue')])
            win.move(1,1)
            if inp:
                if inp in ORDINAL:
                    win.addch(chr(inp))
                else:
                    for key,val in SKEYS.iteritems():
                        if inp in val:
                            win.addstr(key)
                            break
                    else:
                        win.addstr(str(inp))
            win.noutrefresh()
            curses.doupdate()
            inp = win.getch()
    except (curses.ERR, _curses.ERR, curses.error, _curses.error):
        pass

def demo_1(win):
    """Print all available colors with different attributes."""
    win.erase()
    win.box()
    win.bkgd(' ', pairs[('white','black')])
    try:
        for every in ATTRS:
            if every != 'invis':
                for each in pairs:
                    win.addstr(':'.join([str(each), every]), ATTRS[every] | pairs[each])
    except (curses.ERR, _curses.ERR, curses.error, _curses.error):
        pass
    win.noutrefresh()
    curses.doupdate()
    win.getch()

def demo_2(win):
    """Ask user for custom mask."""
    curses.echo()
    try:
        mask = '0x0'
        while 1:
            win.erase()
            win.box()
            win.bkgd(' ', pairs[('white','black')])
            win.move(1,1)
            win.addstr('ABCDEFGHI, 0x0', 0)
            win.move(2,1)
            win.addstr('ABCDEFGHI, %s' % mask, int(mask,16))
            win.noutrefresh()
            curses.doupdate()
            win.move(3,1)
            mask = win.getstr()
            win.move(3,1)
    except:
        pass
    curses.noecho()

def demo_3(win):
    """Explore all masks."""
    done = 0
    mask = 0
    while 1:
        try:
            win.erase()
            win.box()
            win.bkgd(' ', pairs[('white','black')])
            while 1:
                win.addstr(' ABCD %s ' % hex(mask<<8), mask<<8)
                if mask <= 0:
                    mask = 1
                elif mask >= 0xffffffff:
                    done = 1
                else:
                    mask += 1
                if done:
                    break
        except (curses.ERR, _curses.ERR, curses.error, _curses.error):
            win.getch()
        if done:
            break
    win.noutrefresh()

def demo_4(win):
    """Print single lines."""
    win.erase()
    win.box()
    win.bkgd(' ', pairs[('white','black')])
    try:
        win.move(1,1)
        win.addstr("What is this??", ATTRS['uline'] | pairs['yellow','pink'])
        win.move(3,1)
        win.addstr("What is this??", ATTRS['uline'] | pairs['orange','lgray'])
        win.getch()
    except (curses.ERR, _curses.ERR, curses.error, _curses.error):
        pass
    win.noutrefresh()

def demo_5(win, inp):
    """Cursor movement."""
    ymin,xmin = 0,0
    ymin += 1
    xmin += 1
    ymax,xmax = win.getmaxyx()
    ymax -= 2
    xmax -= 2
    x = 1
    y = 1
    win.erase()
    win.bkgd(' ', pairs[('black','lgray')])
    win.box()
    if inp is not None and inp > -1:
        if inp in SKGROUPS['ARROW']:
            if inp in SKEYS['UP']:
                y = max(y-1,ymin)
            elif inp in SKEYS['DOWN']:
                y = min(y+1, ymax)
            elif inp in SKEYS['LEFT']:
                x = max(x-1, xmin)
            elif inp in SKEYS['RIGHT']:
                x = min(x+1, xmax)
            win.addch(y, x, 'X')
        elif inp in SKEYS['MOUSE']:
            _, mx, my, _, click = curses.getmouse()
            if click in SGL_CLICKS:
                if win.enclose(my,mx):
                    # rev = not rev
                    win.addstr(y, x, str((mx,my,click)))
    win.noutrefresh()


class Desktop(object):
    def __init__(self, fg='white', bg='blue'):
        self.window = None
        self.windows = []
        self.fg = fg
        self.bg = bg
        self.ymax = 0
        self.xmax = 0
        self.shadow = True
        self.initted = False
        self.ended = False
        self.getch = None
        self.my = None
        self.mx = None
        self.click = None

    def build(self):
        pass

    def run(self):
        try:
            self.init()
            self.build()
            self.updateloop()
        except (curses.ERR, _curses.ERR, curses.error, _curses.error):
            raise
        except KeyboardInterrupt:
            self.end_win()
        except Exception:
            self.end_win()
            raise

    def init(self):
        self.window = curses.initscr()
        self.initted = True
        self.ymax, self.xmax = self.window.getmaxyx()
        terminfo = curses.longname()
        assert '256' in terminfo  # your env TERM must be xterm-256color!
        assert curses.has_colors()
        curses.start_color()
        curses.use_default_colors()
        ctr = 1
        for fg in CLRS:
            for bg in CLRS:
                if ctr <= curses.COLORS-1 and fg != bg:
                    curses.init_pair(ctr, CLRS[fg], CLRS[bg])
                    pairs[(fg,bg)] = curses.color_pair(ctr)
                    ctr += 1
        curses.meta(1)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.delay_output(0)
        curses.mouseinterval(150)
        availmask,_ = curses.mousemask(curses.ALL_MOUSE_EVENTS)
        assert availmask != 0  # mouse must be available!
        self.window.leaveok(1)
        self.window.scrollok(0)
        self.window.keypad(1)
        if NONBLOCKING:
            self.window.nodelay(1)
            self.window.timeout(NONBLOCKING_TIMEOUT)
        else:
            self.window.nodelay(0)
            self.window.timeout(-1)
        self.window.refresh()

    def redraw(self):
        self.window.bkgd(' ', pairs[(self.fg, self.bg)])
        for each in self.windows:
            if self.shadow:
                self.draw_shadow(each)
        self.window.noutrefresh()
        for each in self.windows:
            each.redraw()
        curses.doupdate()

    def updateloop(self):
        while True:
            self.redraw()
            self.getch = self.window.getch()
            self.mx, self.my, self.click = None, None, None
            if self.getch:
                if self.getch > -1:
                    if self.getch in SKEYS['MOUSE']:
                        _, self.mx, self.my, _, click = curses.getmouse()
                        for each in self.windows:
                            if each.window.enclose(self.my, self.mx):
                                each.on_click(self.my, self.mx)

    def draw_shadow(self, window):
        self.window.hline(window.y+window.ymax, window.x+1, ' ', window.xsize, pairs['white', 'black'])
        self.window.vline(window.y+1, window.x+window.xmax, ' ', window.ysize, pairs['white', 'black'])

    def __del__(self):
        self.end_win()

    def end_win(self):
        if self.initted and not self.ended:
            if self.window:
                self.window.leaveok(0)
                self.window.scrollok(1)
                self.window.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            self.ended = True

    def add_win(self, window):
        ysize = min(window.ysize, self.ymax - window.y)
        xsize = min(window.xsize, self.xmax - window.x)
        y = min(window.y, self.ymax)
        x = min(window.x, self.xmax)
        newwin = self.window.subwin(ysize, xsize, y, x)
        newwin.refresh()
        window.init(newwin)
        for each in self.windows:
            each.z += 1
        window.z = 0
        self.windows.append(window)

class Window(object):
    def __init__(self, y=1, x=1, ysize=10, xsize=20, fg='black', bg='cream', has_border=True, has_titlebar=True, has_menubar=True):
        self.window = None
        self.has_titlebar = has_titlebar
        self.has_menubar = has_menubar
        selftitleubar = None
        self.menubar = None
        self.fg = fg
        self.bg = bg
        self.y = y
        self.x = x
        self.ysize = ysize
        self.xsize = xsize
    def init(self, window):
        self.window = window
        self.ymax, self.xmax = self.window.getmaxyx()
        if self.has_titlebar:
            self.titlebar = self.window.derwin(1, self.xmax, 0, 0)
        if self.has_menubar:
            self.menubar = self.window.derwin(1, self.xmax, 1, 0)
    def redraw(self):
        self.window.bkgd(' ', pairs[(self.fg, self.bg)])
        self.window.noutrefresh()
        if self.has_titlebar:
            if self.z == 0:
                self.titlebar.bkgd(' ', pairs[('white', 'cyan')])
            else:
                self.titlebar.bkgd(' ', pairs[('gray', 'green')])
            self.titlebar.noutrefresh()
        if self.has_menubar:
            self.menubar.bkgd(' ', pairs[('black', 'lgray')])
            self.menubar.noutrefresh()
    def on_click(self, my, mx):
        self.window.addstr(6, 8, str(self.has_titlebar))

class MenuBar(Window):
    def __init__(self):
        self.items = []
    def redraw():
        pass

class MyDesktop(Desktop):
    def build(self):
        myWin = Window()
        self.add_win(myWin)
        myWin2 = Window(5, 5)
        self.add_win(myWin2)
md = MyDesktop()
md.run()
del md

# try:
#     bar = scr.subwin(1, xmax, 0, 0)
#     scr.hline(0, 0, ' ', xmax, pairs['black', 'lgray'])
#     win = scr.subwin(10,20,2,4)
#     inp = None
#     while 1:
#         demo_5(win, inp)
#         scr.hline(12, 5, ' ', 20, pairs['white', 'black'])
#         scr.vline(3, 24, ' ', 10, pairs['white', 'black'])
#         bar.bkgd(' ', pairs[('black','lgray')])
#         bar.addch(0, 1, 'F', ATTRS['uline'])
#         bar.addstr(0, 2, 'ile')
#         bar.noutrefresh()
#         scr.noutrefresh()
#         curses.doupdate()
#         inp = scr.getch()
# except (curses.ERR, _curses.ERR, curses.error, _curses.error):
#     raise
