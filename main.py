#!/usr/bin/env python

"""Conway's Game of Life - in Python
    I know. Totally original project idea, right?"""

__author__ = "Adam Xu(adx59)"
__status__ = "Development"

# import tkinter & time
from tkinter import *
import time

# iteration count
iCount = 0


class GolCell(Button):
    def __init__(self, master, x, y):
        """GolCell(master, x, y) -> None
            creates new Game of Life Cell"""
        # initialize button
        Button.__init__(self, width=2, height=1, relief='groove', bg='white', command=self.pop)
        self.popped = False
        self.x, self.y = x, y
        # bind to unpop function, right click to unpopulate
        self.bind('<Button-3>', self.unpop)

    def pop(self):
        """G.pop() -> None
            populates Game of Life Cell"""
        self.popped = True
        # cosmetic
        self['bg'] = "blue"

    def unpop(self, bind):
        """G.unpop() -> None
            unpopulates Game of Life Cell"""
        self.popped = False
        # cosmetic
        self['bg'] = "white"


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
        clearScrButton = Button(text = "Clr", relief='groove', command=self.clearGrid,
                                width=4, height=1).grid(row=4, column = self.yl)
        

    def iterate(self):
        """g.iterate() -> None
            iterates the grid by one 'life cycle'
            cells that are to be unpopulated are unpopulated,
            and vice versa"""
        # iteration count, add to iteration count
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
                if srrPop < 2:
                    coordsToUPop.append((x, y))
                elif srrPop == 2:
                    pass
                elif srrPop == 3:
                    coordsToPop.append((x, y))
                elif srrPop > 3:
                    coordsToUPop.append((x, y))
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
            continously do iterations of the grid, with an interval of
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
        
    def export(self, filename):
        file = open(filename, 'w')
        

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
        # t button sets the interval
        elif event.char == 't':
            g.setItvl()


root = Tk()
root.title('Game Of Life')
# setup grid
# adjust grid size here
g = golGrid(root, 20, 20, 200)
g.grid()
#bind, and mainloop
root.bind("<Key>", g.pressed)
root.mainloop()
