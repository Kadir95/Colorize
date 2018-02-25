from ColorPalette import *
from tkinter import *

root = Tk()

obj = ColorPalette("Colors.palette")

frame = obj.frame(root=root, row=2, size=(40, 4))

frame.pack()

root.mainloop()