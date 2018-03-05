from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from colorPalette import *
import layering
from PIL import Image, ImageTk
import numpy
import random

stdsize = (1920, 1080)
stdfalldown = 190

currentphotofilepath    = None
currentphoto            = None
currentlayer            = None
currentcolor            = ((255, 0, 0), '#ff0000')
colorpalettefile        = None
colorpaletteOBJ         = None

imageColorSelection = False

def openfile():
    filedir = filedialog.askopenfile(title='Choose Image File', filetypes=[("Image",("*.img","*.jpg","*.png"))])
    if filedir is not None:
        print ("Opening File : ", filedir.name)
        return filedir.name
    return

def savefile():
    if currentlayer is None or currentcolor is None or currentphoto is None:
        if currentlayer is None:
            print("Current layer Doesn't Found")
        if currentphoto is None:
            print("Current photo Doesn't Found")
        if currentcolor is None:
            print("Current color Doesn't Found")
        return
    savedialog = filedialog.asksaveasfile(mode="w", title="Save Image", defaultextension=".jpg", filetypes=[("Image", ("*.jpg"))])
    if savedialog is None:
        return
    currentlayer.currentImage().save(savedialog.name, "JPEG", quality=100)
    savedialog.close()

def converttoGrayscale(image):
    return image.convert('L')

def converttobalckandwhite(image):
    image = converttoGrayscale(image)
    image = numpy.array(image, dtype=numpy.uint8)

    image[image < stdfalldown] = 0
    image[image >= stdfalldown] = 255

    image = Image.fromarray(image)
    return image

def resizeImage(image, size = None, ratio=True):
    if size is not None:
        percente = 1
        if ratio:
            if image.size[0] >= image.size[1]:
                percente = (size[0] / float(image.size[0]))
            else:
                percente = (size[1] / float(image.size[1]))
            image = image.resize((int(image.size[0] * percente), int(image.size[1] * percente)), Image.ANTIALIAS)
        else:
            image = image.resize((size[0], size[1]), Image.ANTIALIAS)
    return image

def openimage(photofile):
    global currentphotofilepath
    currentphotofilepath = photofile
    return Image.open(photofile)

def tkPhoto(image):
    global currentphoto
    currentphoto = image
    return ImageTk.PhotoImage(image)

def displayPhoto(event=None, file = None):
    if file is None:
        file = openfile()
        if file is None:
            return

    im = openimage(file)

    if im.size[0] > stdsize[0] or im.size[1] > stdsize[1]:
        im = converttobalckandwhite(resizeImage(im, size=stdsize))
    else:
        im = converttobalckandwhite(im)

    photo = tkPhoto(im)

    global currentlayer
    currentlayer = layering.Layer(im)

    if radio_var.get() == 1:
        currentlayer.fourConnectedComponent()
    else:
        currentlayer.eightConnectedComponent()

    labelphoto.configure(image=photo, width=photo.width(), height=photo.height())
    labelphoto.image = photo
    return photo

def labelClick(event):
    global imageColorSelection
    if imageColorSelection:
        pix = currentlayer.currentImage().load()
        colorrgb = pix[event.x, event.y]
        colorhex = "#%02x%02x%02x" %(colorrgb)
        global currentcolor
        currentcolor = (colorrgb, colorhex)
        colorshowlabel.configure(bg=currentcolor[1])
        imageColorSelection = False
        return

    if currentlayer is None or currentcolor is None or currentphoto is None:
        if currentlayer is None:
            print("Current layer Doesn't Found")
        if currentphoto is None:
            print("Current photo Doesn't Found")
        if currentcolor is None:
            print("Current color Doesn't Found")
        return
    image = currentlayer.paint(event.x, event.y, currentcolor)
    image = tkPhoto(image)
    labelphoto.configure(image=image, width=image.width(), height=image.height())
    labelphoto.image = image
    print("x:", event.x, " y:", event.y)

def sliderFunction(value):
    global stdfalldown
    stdfalldown = int(value)

def selectColor(event):
    global currentcolor
    color = colorchooser.askcolor(currentcolor[1])
    if color[0] is not None:
        currentcolor = color
        currentcolor = ((int(currentcolor[0][0]), int(currentcolor[0][1]), int(currentcolor[0][2])), currentcolor[1])
    print("Color : ", color)

    # Color Show Layer init
    colorshowlabel.configure(bg=currentcolor[1])

def UndoFunc(event):
    if currentlayer is None or currentcolor is None or currentphoto is None:
        if currentlayer is None:
            print("Current layer Doesn't Found")
        if currentphoto is None:
            print("Current photo Doesn't Found")
        if currentcolor is None:
            print("Current color Doesn't Found")
        return
    image = currentlayer.undo()
    image = tkPhoto(image)
    labelphoto.configure(image=image, width=image.width(), height=image.height())
    labelphoto.image = image

def RedoFunc(event):
    if currentlayer is None or currentcolor is None or currentphoto is None:
        if currentlayer is None:
            print("Current layer Doesn't Found")
        if currentphoto is None:
            print("Current photo Doesn't Found")
        if currentcolor is None:
            print("Current color Doesn't Found")
        return
    image = currentlayer.redo()
    image = tkPhoto(image)
    labelphoto.configure(image=image, width=image.width(), height=image.height())
    labelphoto.image = image

def ColorPaletteColorSelecitonFunc(event):
    colorhex = event.widget["background"]
    colorrgb = tuple(int(colorhex[1:][i: i+2], 16) for i in (0, 2, 4))
    global currentcolor
    currentcolor = (colorrgb, colorhex)
    colorshowlabel.configure(bg=currentcolor[1])

def RandomFill(event):
    currentlayer.takeUndoStrack()
    for i in currentlayer.layerlist:
        choosencolor = random.choice(colorpaletteOBJ.colors)
        i.giveColor(choosencolor)

    image = currentlayer.refreshImage()
    image = tkPhoto(image)
    labelphoto.configure(image=image, width=image.width(), height=image.height())  # , width=im[1], height=im[2])
    labelphoto.image = image
    return

def ClearButtonFunc():
    currentlayer.takeUndoStrack()
    for i in currentlayer.layerlist:
        i.giveColor(((255, 255, 255), "#ffffff"))

    image = currentlayer.refreshImage()
    image = tkPhoto(image)
    labelphoto.configure(image=image, width=image.width(), height=image.height())  # , width=im[1], height=im[2])
    labelphoto.image = image
    return

def imageColorSelectionButtonFunc():
    global imageColorSelection
    imageColorSelection = True
    return

# Root tk object and basic windows  settings
root = Tk()
root.title("Colorize")
root.resizable(False, False)

# right side color palette image loading
colorpalettefile = "Colors.palette"

# Image display label
labelphoto = Label(root)

topframe = Frame(root)
leftframe = Frame(root)

# Configure Frame
conframe = Frame(topframe)

# Open File and Select Color buttons
button = Button(conframe, text='Open File')
buttoncolor = Button(conframe, text='Select Color')

# Redo and Undo Frame
ruFrame = Frame(topframe)

# Undo and Redo Buttons
undoButton = Button(ruFrame, text="Undo")
redoButton = Button(ruFrame, text="Redo")

# Save Image Button
saveImageButton = Button(topframe, text="Save", command=savefile)

# Radio Button's frame
radioFrame = Frame(topframe)

# Radio Buttons
radio_var = IntVar(value=2)
four_connected_radiobutton = Radiobutton(radioFrame, text="Four Connected", variable=radio_var, value=1).pack(fill=X)
eight_connected_radiobutton = Radiobutton(radioFrame, text="Eight Connected", variable=radio_var, value=2).pack(fill=X)

# Slider
scale = Scale(topframe, from_=0, to=255, orient=HORIZONTAL, command=sliderFunction)
scale.set(stdfalldown)

# Open file and Select Color buttons pack
button.grid(row=0, column=0, sticky=W+E)
buttoncolor.grid(row=1, column=0, sticky=W+E)

# Undo Button packing
undoButton.grid(row=0, column=0, sticky=W+E)
redoButton.grid(row=1, column=0, sticky=W+E)

# Random Fill Button
randomfillbutton = Button(topframe, text="Random\nFill")

# Clear Button
clearbutton = Button(topframe, text="Clear", command=ClearButtonFunc)

# Show color selection
colorshowlabel = Label(leftframe, width=5, height=3, bg=currentcolor[1])

# Color selection from image
imageColorSelectionButton = Button(leftframe, text="Pick\nColor", command=imageColorSelectionButtonFunc)

# Color Selection Palette
colorpaletteOBJ = ColorPalette(colorpalettefile)
colorselectionpaletteframe = colorpaletteOBJ.frame(root=leftframe, row=None, column=4, size=(11, 700/28), command=ColorPaletteColorSelecitonFunc)


# slider pack
scale.grid(row=0, column=2)

# Open file and Select Color buttons functions
button.bind('<Button-1>', displayPhoto)
buttoncolor.bind('<Button-1>', selectColor)

# Undo Button function
undoButton.bind('<Button-1>', UndoFunc)
redoButton.bind('<Button-1>', RedoFunc)

# Random Fill Button packing and Func
randomfillbutton.grid(row=0, column=6, sticky=E+N+S)
randomfillbutton.bind('<Button-1>', RandomFill)

# Clear Button packing
clearbutton.grid(row=0, column=7, sticky=E+N+S)

# Save Image Button packing
saveImageButton.grid(row=0, column=5, sticky=E+N+S)

# Label packing and function
labelphoto.grid(row=1, column=0)
labelphoto.bind('<Button-1>', labelClick)

# Color Show label
colorshowlabel.grid(row=2, column=0, sticky=S)

# İmage pick up button pack
imageColorSelectionButton.grid(row=0, column=0, sticky=W+E)

# Color Palette label pack and func
colorselectionpaletteframe.grid(row=1, column=0, sticky=N+S)

# Frames packing
topframe.grid(row=0, column=0, columnspan=2, sticky=E+W)
leftframe.grid(row= 1, column=1, sticky=N+S+E)
conframe.grid(row=0, column=0, sticky=W)
radioFrame.grid(row=0, column=3, sticky=E)
ruFrame.grid(row=0, column=4, sticky=E)

# default image loading
displayPhoto(file='JPG-logo-highres_400x400.jpg')

# Main Loop
root.mainloop()
