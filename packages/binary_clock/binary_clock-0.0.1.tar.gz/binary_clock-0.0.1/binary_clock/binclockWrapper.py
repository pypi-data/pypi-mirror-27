#!/usr/bin/env python2.5

"""This module defines a binary clock, with display.

The clock is a row of cells. They represent in binary
the number of "ticks" elapsed since the beginning of the
day.

"""

from __future__ import division

import sys
import sched
import time
import tkinter
import argparse
import numpy as np
from PIL import Image, ImageTk


# ************************ CONSTANTS ************************

SECSDAY = 24 * 60 * 60  # Seconds per day
# Now, the difference in hours between system time and local time:
SEASONCORR = time.localtime().tm_hour - time.gmtime(time.time()).tm_hour


# ************************ CLASSES ************************

class Win(tkinter.Tk):
    """Class to make frames draggable."""
    # Simplification of code found in https://stackoverflow.com/questions/29641616/drag-window-when-using-overrideredirect

    def __init__(self, master=None):
        tkinter.Tk.__init__(self, master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<B1-Motion>', self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x, y=y))



class BinaryClock(tkinter.Frame):
    """Class that inherits the Frame representation and contains the logic of the clock."""
    def __init__(self, geom, image_on, image_off, borderwidth, bgcolor, master=None):
        tkinter.Frame.__init__(self, master)
        self.geom = geom
        self.borderwidth = borderwidth
        self.bgcolor = bgcolor
        self.pack(padx=1, pady=1)
        self.nbTicks = 2**self.nbBits
        self.master.title("Binary Clock 0.0.1")
        self.scheduler = sched.scheduler(myTime, time.sleep)
        self.images = dict(
            on=ImageTk.PhotoImage(colorTransparency(image_on, "#000000"), master=master),
            off=ImageTk.PhotoImage(colorTransparency(image_off, "#000000"), master=master),
        )
        self.createWidgets()

    @property
    def nbRows(self):
        n, _ = self.geom
        return n

    @property
    def nbCols(self):
        _, n = self.geom
        return n

    @property
    def nbBits(self):
        return self.nbRows * self.nbCols

    def createWidgets(self):
        """Creates the bit labels in the clock."""
        self.bits = []
        for i in range(self.nbRows):
            frame = tkinter.Frame(self, bg=self.bgcolor)
            frame.pack(padx=0, pady=0)
            for j in range(self.nbCols):
                newBit = tkinter.Label(frame,
                                       image=self.images['off'],
                                       relief=tkinter.SOLID,
                                       borderwidth=self.borderwidth,
                                       highlightthickness=0,
                                       highlightcolor='#000000',
                                       highlightbackground='#000000',
                                       #highlightcolor=self.bgcolor,
                                       #highlightbackground=self.bgcolor,

                                       )
                newBit.pack(side=tkinter.LEFT, padx=1, pady=1)
                self.bits.append(newBit)



    def processTick(self):
        """Updates the clock, then schedules the next tick."""
        self.setToTick()
        self.tick += 1
        if self.tick == self.nbTicks:  # Midnight: a new day starts.
            self.tick = 0
            self.day += 1
        newTime = SECSDAY * (self.day + tick2dayfrac(self.tick, self.nbTicks))
        self.scheduler.enterabs(newTime, 1, self.processTick, ())

    def run(self):
        """Starts the clock."""
        self.day = int(myTime()) // SECSDAY
        self.tick = dayfrac2tick(myTime() / SECSDAY, self.nbTicks)
        self.processTick()
        self.scheduler.run()

    def setToTick(self):
        """Modifies the colors on the clock according to tick, and updates."""
        for (bit, val) in zip(self.bits, binaryForm(self.tick, self.nbBits)):
            if val:
                im = self.images['on']
            else:
                im = self.images['off']
            if str(im) != bit['image']:
                bit.configure(image=im)
        self.update()


    # ********* Other Constructors *********

    @classmethod
    def buildFlatSquare(cls, geom, side, col_empty, col_used, bgcolor, borderwidth, master=None):
        """Constructer in flat color mode."""
        return cls(geom=geom,
                   image_on=buildRectangleImage(side_w=side, col=col_used),
                   image_off=buildRectangleImage(side_w=side, col=col_empty),
                   borderwidth=borderwidth,
                   bgcolor=bgcolor,
                   master=master,
                   )


# ************************ FUNCTIONS ************************

def myTime():
    """Returns local time in seconds since an epoch at 00:00:00."""
    return time.time() + SEASONCORR * 3600

def tick2dayfrac(tick, nbTicks):
    """Conversion tick -> day fraction."""
    return tick / nbTicks

def dayfrac2tick(fd, nbTicks):
    """Conversion day fraction -> tick."""
    return int( (fd % 1) * nbTicks)

def binaryForm(n, nbDigs=0):
    """Generates the bits of n in binary form.

    If the sequence has less than nbDigs digits, it is left-padded with zeros.
    """
    digits = []
    while n:
        digits.append(n & 1)
        n >>= 1
    return reversed(digits + [0]*(nbDigs - len(digits)))


def colstr2tuple(colstr):
    """Conterts a '#rrggbb' string to RGB 0-255 triple."""
    red = int("0x" + colstr[1:3], base=16)
    green = int("0x" + colstr[3:5], base=16)
    blue = int("0x" + colstr[5:7], base=16)
    return red, green, blue


def buildRectangleImage(col, side_w, side_h=None):
    """Returns a tkinter.Image with a flat-color rectangle."""
    if side_h is None:
        side_h = side_w
    red = int("0x" + col[1:3], base=16)
    green = int("0x" + col[3:5], base=16)
    blue = int("0x" + col[5:7], base=16)
    arr = np.zeros(shape=(side_h, side_w, 4), dtype=np.uint8)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue
    arr[:, :, 3] = 255
    return Image.fromarray(arr)


def colorTransparency(img, bgcolor):
    """Returns a tkinter.Image with background color bgcolor and img superimposed."""
    if img.mode == 'RBGA':
        img_w, img_h = img.size
        red, green, blue = colstr2tuple(bgcolor)
        background = Image.new('RGBA', (img_w, img_h), (red, green, blue, 255))
        background.paste(img, (0, 0), img)
        return background
    else:
        return img


def binclock_wrapper(arg_list):
    # ***** Parser *****
    parser = argparse.ArgumentParser(
        prog="binclock",
        description="Truly Binary Clock",
    )
    parser.add_argument('--offset', help="Initial window offset from right-bottom corner", default='-1-43')
    parser.add_argument('--color', help="Bits color", default='#00d0ff')
    parser.add_argument('--bgcolor', help="Borders color", default='#d0d0d0')
    parser.add_argument('--side', help="Pixels per side of each bit", type=int, default=10)
    parser.add_argument('--borderwidth', help="Pixels per border for bits", type=int, default=2)
    parser.add_argument('--imageon', help="Image for used bits. If present, overrides color/size", default=None)
    parser.add_argument('--imageoff', help="Image for bits not used.  If present, overrides color/size", default=None)
    parser.add_argument('--geometry', help="Rows x Columns size", default='1x16', type=lambda s: tuple(int(e) for e in s.lower().split('x')))
    parser.add_argument('--persistent', help="If present, make the clock overlap on other windows", action='store_true')

    args = parser.parse_args(arg_list)

    root = Win()
    root.resizable(False, False)  # Window not resizable
    root.overrideredirect(True)  # No Bar, window can be dragged.
    root.geometry(args.offset)  # Window located in the bottom-right corner, with the given offset
    root.configure(background=args.bgcolor)
    #root.configure(background='#000000')

    if args.persistent:
        try:  # This block works (and is necessary) in MS-Windows only.
            root.attributes('-topmost', True)  # So that the clock cannot be hidden by any window.
        except tkinter.TclError:
            pass

    if args.imageon is None:
        BinaryClock.buildFlatSquare(
            geom=args.geometry,
            side=args.side,
            borderwidth=args.borderwidth,
            bgcolor=args.bgcolor,
            col_empty='#000000',
            col_used=args.color,
            master=root
        ).run()
    else:
        BinaryClock(
            geom=args.geometry,
            image_on=Image.open(args.imageon),
            image_off=Image.open(args.imageoff),
            borderwidth=args.borderwidth,
            bgcolor=args.bgcolor,
            master=root
        ).run()

