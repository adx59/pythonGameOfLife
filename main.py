#!/usr/bin/env python

"""Conway's Game of Life - in Python
    I know. Totally original project idea, right?"""

__author__ = "Adam Xu(adx59)"
__status__ = "Development"

# import tkinter & time
from tkinter import *
from tkinter import messagebox
import time
import os

# iteration count
iCount = 0
# config data list
data = [None] * 7


def loadConfig():
    """loadConfig -> None
        loads data from configuration file(CONFIG.txt)"""
    global data
    cfile = open('CONFIG.txt', 'r')
    data[0] = cfile.readline().strip()
    data[1] = cfile.readline().strip()
    data[2] = int(cfile.readline())
    data[3] = int(cfile.readline())
    dlpData = cfile.readlines()
    data[4] = eval(dlpData[0].strip())
    data[5] = eval(dlpData[1].strip())
    data[6] = eval(dlpData[2].strip())
    print(data)


loadConfig()


class GolCell(Button):
    def __init__(self, master, x, y):
        """GolCell(master, x, y) -> None
            creates new Game of Life Cell"""
        # initialize button
        global data
        Button.__init__(self, width=2, height=1, relief='groove', bg=data[1], command=self.pop)
        self.popped = False
        self.x, self.y = x, y
        # bind to unpop function, right click to unpopulate
        self.bind('<Button-3>', self.unpop)

    def pop(self):
        """G.pop() -> None
            populates Game of Life Cell"""
        global data
        self.popped = True
        # cosmetic
        self['bg'] = data[0]

    def unpop(self, bind):
        global data
        """G.unpop() -> None
            unpopulates Game of Life Cell"""
        self.popped = False
        # cosmetic
        self['bg'] = data[1]


class golGrid(Frame):
    def __init__(self, master, xl, yl, interval):
        """golGrid(master, xlength, ylength, iterationInterval) -> None
            creates new grid of Game of Life cells"""
        # iteration count var
        global iCount
        # init frame
        Frame.__init__(self, master)
        # attributes
        self.m = master
        self.xl = xl
        self.yl = yl
        self.st = True
        # interval of time between iterations
        self.i = interval
        self.p = False
        # dict of gol cells
        self.cells = {}
        # generate grid
        for x in range(xl):
            for y in range(yl):
                self.cells[(x, y)] = GolCell(self, x, y)
                self.cells[(x, y)].grid(row=x, column=y)
        # button to iterate
        iButton = Button(text='Iter', command=self.iterate, relief='groove',
                         width=4, height=1).grid(row=0, column=self.yl)
        # button to change interval
        sIButton = Button(text="Itvl", command=self.setItvl, relief='groove',
                          width=4, height=1).grid(row=1, column=self.yl)
        # button to stop play
        stopButton = Button(text="Stop", relief='groove', command=self.stop,
                            width=4, height=1).grid(row=3, column=self.yl)
        # button to play simulation
        playButton = Button(text="Play", relief='groove', command=self.play,
                            width=4, height=1).grid(row=2, column=self.yl)
        # button to clear screen
        clearScrButton = Button(text="Clr", relief='groove', command=self.clearGrid,
                                width=4, height=1).grid(row=4, column=self.yl)
        impButton = Button(text="Imp.", relief='groove', command=self.importGui,
                           width=4, height=1).grid(row=5, column=self.yl)
        expButton = Button(text="Exp.", relief='groove', command=self.exportGui,
                           width=4, height=1).grid(row=6, column=self.yl)

    def iterate(self):
        """g.iterate() -> None
            iterates the grid by one 'life cycle'
            cells that are to be unpopulated are unpopulated,
            and vice versa"""
        # iteration count, add to iteration count
        global data
        global iCount
        iCount += 1
        # show iteration count in se corner
        iCText = Label(text=str(iCount)).grid(row=self.xl - 1, column=self.yl)
        # arrays of cells to unpopulate and populate
        coordsToUPop = []
        coordsToPop = []
        # scan through all cells in grid
        for x in range(self.xl):
            for y in range(self.yl):
                # amt surrounding cells that are populated
                srrPop = 0
                # coordinates of surrounding cells
                sCellsCoords = [(x, y - 1), (x, y + 1), (x + 1, y), (x - 1, y),
                                (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
                # get rid of coords of cells that don't exist
                for c in sCellsCoords:
                    if c[0] < 0 or c[1] < 0 or c[0] > self.yl or c[0] > self.yl:
                        sCellsCoords.remove(c)
                # find amt of cells populated surrounding
                for c in sCellsCoords:
                    if c[0] > 0 and c[1] > 0 and c[1] <= self.yl - 1 and c[0] <= self.xl - 1:
                        if self.cells[c].popped:
                            srrPop += 1
                # determine what happens to the cell
                if srrPop in data[4]:
                    coordsToUPop.append((x, y))
                elif srrPop in data[5]:
                    pass
                elif srrPop in data[6]:
                    coordsToPop.append((x, y))
        # finally, unpopulate & populate cells
        for coords in coordsToUPop:
            self.cells[coords].unpop(2)
        for coords in coordsToPop:
            self.cells[coords].pop()

    def stop(self):
        """g.stop -> None
            stop the playing of the simulation, if it is"""
        self.st = True

    def play(self):
        """g.play -> None
            continuously do iterations of the grid, with an interval of
            time between each iteration"""
        # start loop
        self.st = False
        # convert ms to s, for the interval
        interval = self.i / 1000
        while not self.st:
            # iterate
            g.iterate()
            # update the display
            self.m.update()
            # sleep the amount of time for the interval
            time.sleep(interval)

    def setItvl(self):
        """g.setItvl -> None
            set the interval for the play function"""
        # open new window
        iWindow = Toplevel(self.m)
        # create entry tk variable
        interval = StringVar()

        # set the interval based on the input in the Entry box
        def set():
            self.i = int(interval.get())

        # label, entry box, and set button
        Label(iWindow, text="Set interval(ms)").grid(row=0, column=0)
        Entry(iWindow, textvariable=interval, width=10).grid(row=1, column=0)
        Button(iWindow, text="Set", command=set, width=5, relief='groove').grid(row=1, column=1)

    def clearGrid(self):
        """g.clearGrid(self) -> None
            clears the grid of populated
            cells"""
        global iCount
        for x in range(self.xl):
            for y in range(self.yl):
                self.cells[(x, y)].unpop(1)
        iCount = 0

    def importfile(self, filename):
        """g.importfile -> None
            imports a .golp file as the grid"""
        g.clearGrid()
        file = open(filename, 'r')
        asciiGridList = file.readlines()
        if len(asciiGridList[1]) - 1 != self.yl:
            messagebox.showerror(title="Aw, Man!", message="Darnet! Exported grid not the same size as current grid")
            return 0
        for y in range(len(asciiGridList)):
            for x in range(len(asciiGridList[y]) - 1):
                if asciiGridList[y][x] == 'X':
                    self.cells[(y, x)].pop()
                elif asciiGridList[y][x] == '`':
                    pass

    def export(self, filename):
        """g.export() -> None
            exports the grid as a .golp file
            the file can be imported in order to set
            the grid accordingly"""
        file = open(filename, 'w')
        for x in range(self.xl):
            for y in range(self.yl):
                if self.cells[(x, y)].popped:
                    file.write('X')
                else:
                    file.write('`')
                if y == self.yl - 1:
                    file.write('\n')

    def exportGui(self):
        """g.exportGui -> None
            opens a GUI for exporting grid"""
        eWindow = Toplevel(self.m)
        filename = StringVar()

        def exp():
            fn = filename.get()
            if '.' in fn:
                self.export(fn)
            else:
                self.export(fn + '.golp')

        Label(eWindow, text="    Filename    ").grid(row=0, column=0)
        Entry(eWindow, textvariable=filename, width=10).grid(row=1, column=0)
        Button(eWindow, text="Export", relief='groove', command=exp, width=7).grid(row=1, column=1)

    def importGui(self):
        """g.import"""
        imWindow = Toplevel(self.m)
        filename = StringVar()

        def imp():
            fn = filename.get()
            if '.' in fn:
                if not os.path.isfile(fn):
                    messagebox.showerror("Oh shoot", "That file isn't in this folder!")
                    return 0
                self.importfile(fn)
            else:
                if not os.path.isfile(fn + '.golp'):
                    messagebox.showerror("Oh shoot", "That file isn't in this folder!")
                    return 0
                self.importfile(fn + '.golp')

        Label(imWindow, text="    Filename    ").grid(row=0, column=0)
        Entry(imWindow, textvariable=filename, width=10).grid(row=1, column=0)
        Button(imWindow, text="Import", relief='groove', command=imp, width=7).grid(row=1, column=1)

    def pressed(self, event):
        """g.pressed -> None
            the bind function for detecting keys
            does something based on what is pressed"""
        # i button iterates the grid
        if event.char == 'i':
            g.iterate()
        # p button starts playing
        elif event.char == 'p':
            g.play()
        elif event.char == 's':
            g.stop()
        # t button sets the interval
        elif event.char == 't':
            g.setItvl()
        elif event.char == 'e':
            g.exportGui()
        elif event.char == 'r':
            g.importGui()


root = Tk()
root.title('Game Of Life')
# setup grid
# adjust grid size here
g = golGrid(root, data[2], data[3], 200)
g.grid()
# bind, and mainloop
root.bind("<Key>", g.pressed)
root.mainloop()
