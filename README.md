# GOL(python)
Game of Life by John Conway-implemented in Python.

# Keyboard Controls

i = Do Iteration

p = Play

s = Stop

t = Set Iteration Interval

e = Export grid

r = Import grid

# Import/Export Capability

Alright, so I got bored, so I added a feature where you can export the grid into a text file. You can also
import the exported files to get your grid that you exported back. But of course, I'm using a different format 
when exporting - .golp. I don't know why. J-just roll w/ it. The code can still read through text files though.

# CONFIG.txt

Ok, so you can actually edit attributes of the board through CONFIG.txt. The first line is the color of populated
cells. The second line is the color of unpopulated cells. The third and fourth line are the width and length of 
the board, and finally the 5th, 6th, and 7th customize the rules of the game. The fifth line is a list of the 
amount of neighboring populated cells that would make a cell unpopulated. The 6th line is a list of the amount of 
neighboring populated cells that would let the cell stay living, and the 7th a list of the amount that would populate
a cell.



