import numpy
import copy

class Number:                       #This class change the int to a reference type
    def __init__(self, number=1):
        self.number = int(number)
        self.color  = ((255, 255, 255), "#ffffff")

    def giveColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def change(self, number):
        self.number = int(number)

    def increment(self):
        self.number += 1

    def __copy__(self):
        temp = Number(self.number)
        temp.color = copy.deepcopy(self.color)
        return temp

    def __str__(self):              #Override toString
        return str(self.number)

    def __int__(self):              #Override toInt
        return self.number

    def get(self):
        return self.number

    def __gt__(self, other):        #Grether then
        if self.number > other.number:
            return True
        return False

    def __eq__(self, other):        #Equal
        if self.number == other.number:
            return True
        return False

    def __lt__(self, other):        #Less then
        if self.number < other.number:
            return True
        return False

    def __cmp__(self, other):
        if self.number > other:
            return 1
        elif self.number < other:
            return -1
        else:
            return 0

    def __hash__(self):
        return hash(self.number)

# four and eight connected layering optimization

class Layer:
    def __init__(self, image):
        self.image = image.copy()
        self.imagearray = numpy.array(image)
        self.imagePaint = None
        self.undoStack = []
        self.redoStack = []
        self.array = None
        self.layerlist = None
        self.createArray()

    def paint(self, mx, my, color):
        if self.array is None:
            return self.image

        if self.imagePaint is None:
            self.imagePaint = self.image.copy()
            self.imagePaint = self.imagePaint.convert("RGB")

        if self.imagePaint.width > mx >= 0 and self.imagePaint.height > my >= 0:
            layerToPaint = self.array[my][mx]

            pix = self.imagePaint.load()

            # if the area already colored, do anything
            if pix[mx, my] == color[0]:
                return self.imagePaint

            if layerToPaint.get() == 0:
                return self.imagePaint

            # Undo Stack
            self.undoStack.append(copy.deepcopy(self.layerlist))
            self.redoStack.clear()

            for i in self.layerlist:
                if i.get() == layerToPaint.get():
                    i.giveColor(color=color)

            for y in range(0, len(self.array)):
                for x in range(0, len(self.array[0])):
                    pix[x, y] = self.array[y][x].color[0]

        return self.imagePaint

    def fourConnectedComponent(self):
        layersList = []     #LayerList keeps the references the layers numbers which keeps in a Number object.
        print("Four Layering started")
        for y in range(0, self.array.shape[0]):
            for x in range(0, self.array.shape[1]):          #This loop to arive array's all elements
                up = checkpixel(self.array, x, y - 1)       #up keeps the up pixel
                left = checkpixel(self.array, x - 1, y)     #left pixel
                me = checkpixel(self.array, x, y)           #current pixel

                zero = Number(0)

                if me > zero:   #if our state is 0 do nothing.
                    if up == zero or left == zero:      #if top or left is black
                        if up == zero and left == zero: #if top and left are black take new layer if any one of them is has a layer take it
                            layersList.append(Number(len(layersList) + 1))
                            self.array[y][x] = layersList[len(layersList) - 1]
                        elif up == zero:
                            self.array[y][x] = left
                        elif left == zero:
                            self.array[y][x] = up

                    else:                               #if top and left have a layer
                        if up == left:                  #if their layers are the same, take it
                            self.array[y][x] = up
                        else:                           #if they are diffirent change the up pixel's layer to left pixel's layer
                            self.array[y][x] = up

                            temp = left.get()

                            for i in layersList:
                                if i.number == temp:
                                    i.change(up.get())

        self.layerlist = layersList
        print("Four Layering ended\nOptimizer started")
        self.LayerListOptimizer()
        print("Optimizer ended")

    def eightConnectedComponent(self):
        layerList = []
        print("Eight Layering started")
        for y in range(0, self.array.shape[0]):
            for x in range(0, self.array.shape[1]):
                west = checkpixel(self.array, x - 1, y)
                northwest = checkpixel(self.array, x - 1, y - 1)
                north = checkpixel(self.array, x, y - 1)
                northeast = checkpixel(self.array, x + 1, y - 1)
                me = checkpixel(self.array, x, y)

                zero = Number(0)

                if me > zero:
                    if zeroCount(west, northwest, north, northeast) < 4:
                        whitelist = nonZeros(west, northwest, north, northeast)
                        same, others = samepix(whitelist)

                        if same is None:
                            same = []
                        if others is None:
                            others = []

                        if len(same) == len(whitelist):
                            self.array[y][x] = same[0]

                        elif len(others) == len(whitelist):
                            self.array[y][x] = others[0]
                            for i in range(1, len(others)):
                                temp = others[i].get()
                                for j in layerList:
                                    if j.get() == temp:
                                        j.change(others[0])

                        else:
                            self.array[y][x] = same[0]
                            for i in others:
                                temp = i.get()
                                for j in layerList:
                                    if j.get() == temp:
                                        j.change(same[0].get())

                    else:
                        layerList.append(Number(len(layerList) + 1))
                        self.array[y][x] = layerList[len(layerList) - 1]

        self.layerlist = layerList
        print("Eight Layering ended\nOptimizer started")
        self.LayerListOptimizer()
        print("Optimizer ended")

    def createArray(self):
        self.array = numpy.empty(shape= (len(self.imagearray), len(self.imagearray[0])), dtype=numpy.object)

        one = Number(1)
        zero = Number(0)
        zero.color = ((0, 0, 0), "#000000")

        for i in range(len(self.imagearray)):
            for j in range(len(self.imagearray[0])):
                if self.imagearray[i][j] > 127:
                    self.array[i][j] = one
                else:
                    self.array[i][j] = zero

    def undo(self):
        if len(self.undoStack) > 0:
            self.redoStack.append(copy.deepcopy(self.layerlist))
            self.refreshLayerlist(self.undoStack.pop())
        return self.refreshImage()

    def redo(self):
        if len(self.redoStack) > 0:
            self.undoStack.append(copy.deepcopy(self.layerlist))
            self.refreshLayerlist(self.redoStack.pop())
        return self.refreshImage()

    def takeUndoStrack(self):
        self.undoStack.append(copy.deepcopy(self.layerlist))
        self.redoStack.clear()

    def currentImage(self):
        if self.imagePaint is None:
            return self.image
        return self.imagePaint

    def refreshImage(self):
        if self.imagePaint is None:
            self.imagePaint = self.image.copy()
            self.imagePaint = self.imagePaint.convert("RGB")

        pix = self.imagePaint.load()

        for y in range(0, len(self.array)):
            for x in range(0, len(self.array[0])):
                pix[x, y] = self.array[y][x].color[0]

        return self.imagePaint

    def randrefreshImage(self):
        if self.imagePaint is None:
            self.imagePaint = self.image.copy()
            self.imagePaint = self.imagePaint.convert("RGB")

        pix = self.imagePaint.load()

        for y in range(0, len(self.array)):
            for x in range(0, len(self.array[0])):
                pix[x, y] = self.array[y][x].color[0]

        return self.imagePaint

    def refreshLayerlist(self, newList):
        for i in range(0, len(self.layerlist)):
            self.layerlist[i].number = newList[i].number
            self.layerlist[i].color = newList[i].color

    def LayerListOptimizer(self):
        control = {}
        for i in self.layerlist:
            if control.get(i.number) is None:
                control[i.number] = i

        uniqList = []
        for i in control:
            uniqList.append(control.get(i))
            control[i] = int(len(uniqList) - 1)

        for y in range(0, len(self.array)):
            for x in range(0, len(self.array[0])):
                if self.array[y][x].number == 0:
                    continue
                self.array[y][x] = uniqList[control.get(self.array[y][x].number)]

        self.layerlist = uniqList

def checkpixel(array, x, y):
    if len(array) > y >= 0 and len(array[0]) > x >= 0:
        return array[y][x]
    return Number(0)

def zeroCount(*arguments):
    count = 0
    for i in arguments:
        if i.get() == 0:
            count += 1
    return count

def nonZeros(*arguments):
    result = []
    for i in arguments:
        if i.get() != 0:
            result.append(i)
    return result

def samepix(arguments):
    if len(arguments) < 2:
        return arguments, None
    for i in range(0, len(arguments)):
        list = [arguments[i]]
        j_list = [i]
        for j in range(0, len(arguments)):
            if not j == i:
                if arguments[i] == arguments[j]:
                    list.append(arguments[j])
                    j_list.append(j)
        if len(list) > 1:
            others = []
            for j in range(0, len(arguments)):
                if j not in j_list:
                    others.append(arguments[j])
            return list, others
    return None, arguments