from tkinter import *
import re

def noop(event):
    print(event.widget["background"])
    return

class ColorPalette:
    def __init__(self, colorFile):
        self.color_palette_file = colorFile
        self.colors = []
        self.initColors()

        self.colorframe = None
        #self.labels = []

        for i in self.colors:
            print(i)
        print(len(self.colors))

    def initColors(self):
        colorstext = open(mode="r", file=self.color_palette_file)

        if colorstext is None:
            return

        expression = re.compile('^\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)')
        lines = colorstext.readlines()

        for line in lines:
            result = expression.match(line)
            if result is not None:
                temp = tuple(int(i) for i in result.groups())
                self.colors.append((temp, "#%02x%02x%02x" %(temp)))

    def frame(self,root, row=None, column=None, size=(70,750), command=noop):
        self.colorframe = Frame(root)

        if len(self.colors) < 1:
            return self.colorframe

        if row is None or column is None:
            colornum = len(self.colors)

            if row is None and column is None:
                row = int(colornum / 2)
                if float(colornum - row) > row:
                    colornum = row + 1
                else:
                    colornum = row

            elif row is None:
                if float(colornum / column) > int(colornum / column):
                    row = int(colornum / column) + 1
                else:
                    row = int(colornum / column)
            else:
                if float(colornum / row) > int(colornum / row):
                    column = int(colornum / row) + 1
                else:
                    column = int(colornum / row)

        x_size = int(size[0]/column)
        y_size = int(size[1]/row)

        for x in range(0, column):
            for y in range(0, row):
                if x*row + y >= len(self.colors):
                    break
                print(self.colors[x*row + y] , "  x*row + y:", x*row + y, " x:", x, " y:", y)
                label = Label(self.colorframe, bg=self.colors[x*row + y][1],  width=x_size, height=y_size)
                label.grid(row=y, column=x)
                label.bind('<Button-1>', command)
                #self.labels.append(label)

        return self.colorframe

