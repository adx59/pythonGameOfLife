#!/usr/bin/env python

"""Conway's Game of Life - in Python
    I know. Totally original project idea, right?"""

__author__ = "Adam Xu(adx59)"
__status__ = "3 - Alpha"

from tkinter import *
import time


iCount = 0


class GolCell(Button):
    def __init__(self, master, x, y):
        Button.__init__(self, width=2, height=1, relief='groove', bg='white', command=self.pop)
        self.popped = False
        self.x, self.y = x, y
        self.bind('<Button-3>', self.unpop)

    def pop(self):
        self.popped = True
        self['bg'] = "blue"

    def unpop(self, bind):
        self.popped = False
        self['bg'] = "white"


class golGrid(Frame):
    def __init__(self, master, xl, yl, interval):
        global iCount
        Frame.__init__(self, master)
        self.m = master
        self.xl = xl
        self.yl = yl
        self.st = True
        self.i = interval
        self.p = False
        self.cells = {}
        for x in range(xl):
            for y in range(yl):
                self.cells[(x, y)] = GolCell(self, x, y)
                self.cells[(x, y)].grid(row=x, column=y)
        iButton = Button(text='Iter', command=self.iterate, relief='groove',
                         width=4, height=1).grid(row=0, column=self.yl)
        sIButton = Button(text="Itvl", command=self.setItvl, relief='groove',
                          width=4, height=1).grid(row=1, column=self.yl)
        stopButton = Button(text="Stop", relief='groove', command=self.stop,
                            width=4, height=1).grid(row=3, column=self.yl)
        playButton = Button(text="Play", relief='groove', command=self.play,
                            width=4, height=1).grid(row=2, column=self.yl)

    def iterate(self):
        global iCount
        iCount += 1
        iCText = Label(text=str(iCount)).grid(row=self.xl - 1, column=self.yl)
        coordsToUPop = []
        coordsToPop = []
        for x in range(self.xl):
            for y in range(self.yl):
                srrPop = 0
                sCellsCoords = [(x, y - 1), (x, y + 1), (x + 1, y), (x - 1, y),
                                (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
                for c in sCellsCoords:
                    if c[0] < 0 or c[1] < 0 or c[0] > self.yl or c[0] > self.yl:
                        sCellsCoords.remove(c)
                for c in sCellsCoords:
                    if c[0] > 0 and c[1] > 0 and c[1] <= self.yl - 1 and c[0] <= self.xl - 1:
                        if self.cells[c].popped:
                            if isinstance(self.cells[c], GolCell):
                                srrPop += 1
                if srrPop < 2:
                    coordsToUPop.append((x, y))
                elif srrPop == 2:
                    pass
                elif srrPop == 3:
                    coordsToPop.append((x, y))
                elif srrPop > 3:
                    coordsToUPop.append((x, y))
        for coords in coordsToUPop:
            self.cells[coords].unpop(2)
        for coords in coordsToPop:
            self.cells[coords].pop()

    def stop(self):
        self.st = True

    def play(self):
        self.st = False
        interval = self.i / 1000
        while not self.st:
            g.iterate()
            self.m.update()
            time.sleep(interval)

    def setItvl(self):
        iWindow = Toplevel(self.m)
        interval = StringVar()

        def set():
            self.i = int(interval.get())

        Label(iWindow, text="Set interval(ms)").grid(row=0, column=0)
        Entry(iWindow, textvariable=interval, width=10).grid(row=1, column=0)
        Button(iWindow, text="Set", command=set, width=5, relief='groove').grid(row=1, column=1)

    def pressed(self, event):
        if event.char == 'i':
            g.iterate()
        elif event.char == 'p':
            g.play()
        elif event.char == 't':
            g.setItvl()


root = Tk()
root.title('Game Of Life')
# adjust grid size here
g = golGrid(root, 20, 20, 200)
g.grid()
root.bind("<Key>", g.pressed)
root.mainloop()
