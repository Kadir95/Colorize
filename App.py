from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from ColorPalette import *
import layering
from PIL import Image, ImageTk
import numpy

stdsize = (800, 800)
stdfalldown = 127

currentphotofilepath    = None
currentphoto            = None
currentlayer            = None
currentcolor            = ((255, 0, 0), '#ff0000')
colorpalettefile            = None


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
    image = numpy.array(image)
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] >= stdfalldown:
                image[i][j] = 255
            else:
                image[i][j] = 0
    print(image)
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
    return image, image.size[0], image.size[1]

def openimage(photofile):
    global currentphotofilepath
    currentphotofilepath = photofile
    return Image.open(photofile)

def tkPhoto(image):
    global currentphoto
    currentphoto = image
    return ImageTk.PhotoImage(image)

def displayPhoto(event, file = None):
    im = None
    if file is None:
        #im = resizeImage(converttobalckandwhite(openimage(openfile())), size=stdsize)
        im = converttobalckandwhite(openimage(openfile()))
    else:
        #im = resizeImage(converttobalckandwhite(openimage(file)), size=stdsize)
        im = converttobalckandwhite(openimage(file))

    #im = im[0]
    photo = tkPhoto(im)

    global currentlayer
    currentlayer = layering.Layer(im)

    #layering.printArray(currentlayer.array)
    #print()

    if radio_var.get() == 1:
        currentlayer.fourConnectedComponent()
    else:
        currentlayer.eightConnectedComponent()

    #layering.printArray(currentlayer.array)

    labelphoto.configure(image=photo, width=photo.width(), height=photo.height()) #, width=im[1], height=im[2])
    labelphoto.image = photo
    return photo

def labelClick(event):
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
    labelphoto.configure(image=image, width=image.width(), height=image.height())  # , width=im[1], height=im[2])
    labelphoto.image = image
    print("x:", event.x, " y:", event.y)

def sliderFunction(value):
    print("slider value : ", value)
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
    labelphoto.configure(image=image, width=image.width(), height=image.height())  # , width=im[1], height=im[2])
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
    labelphoto.configure(image=image, width=image.width(), height=image.height())  # , width=im[1], height=im[2])
    labelphoto.image = image

def ColorPaletteColorSelecitonFunc(event):
    colorhex = event.widget["background"]
    colorrgb = tuple(int(colorhex[1:][i: i+2], 16) for i in (0, 2, 4))
    global currentcolor
    currentcolor = (colorrgb, colorhex)
    colorshowlabel.configure(bg=currentcolor[1])

def RandomFill():
    return

# Root tk object and basic windows  settings
root = Tk()
root.title("Image Fill")
root.resizable(False, False)

# right side color palette image loading
colorpalettefile = "Colors.palette"

ima = resizeImage(openimage('JPG-logo-highres_400x400.jpg'), size=stdsize)
photo = tkPhoto(converttobalckandwhite(ima[0]))
labelphoto = Label(root, image=photo, width=ima[1], height=ima[2])
labelphoto.image = photo

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
radio_var = IntVar(value=1)
four_connected_radiobutton = Radiobutton(radioFrame, text="Four Connected", variable=radio_var, value=1).pack()
eight_connected_radiobutton = Radiobutton(radioFrame, text="Eight Connected", variable=radio_var, value=2).pack()

# Slider
scale = Scale(topframe, from_=0, to=255, orient=HORIZONTAL, command=sliderFunction)
scale.set(stdfalldown)

# Open file and Select Color buttons pack
button.grid(row=0, column=0, sticky=W+E)
buttoncolor.grid(row=1, column=0, sticky=W+E)

# Undo Button packing
undoButton.grid(row=0, column=0)
redoButton.grid(row=1, column=0)

# Show color selection
colorshowlabel = Label(leftframe, width=5, height=3, bg=currentcolor[1])

# Color Selection Palette
colorpaletteOBJ = ColorPalette(colorpalettefile)
colorselectionpaletteframe = colorpaletteOBJ.frame(root=leftframe, row=None, column=4, size=(10, 700/28), command=ColorPaletteColorSelecitonFunc)


# slider pack
scale.grid(row=0, column=2)

# Open file and Select Color buttons functions
button.bind('<Button-1>', displayPhoto)
buttoncolor.bind('<Button-1>', selectColor)

# Undo Button function
undoButton.bind('<Button-1>', UndoFunc)
redoButton.bind('<Button-1>', RedoFunc)

# Save Image Button packing
saveImageButton.grid(row=0, column=5, sticky=E+N+S)

# Label packing and function
labelphoto.grid(row=1, column=0)
labelphoto.bind('<Button-1>', labelClick)

# Color Show label
colorshowlabel.grid(row=1, column=0, sticky=S)

# Color Palette label pack and func
colorselectionpaletteframe.grid(row=0, column=0, sticky=N+S)

# Frames packing
topframe.grid(row=0, column=0, sticky=E+W)
leftframe.grid(row= 1, column=1, sticky=N+S)
conframe.grid(row=0, column=0, sticky=W)
radioFrame.grid(row=0, column=3, sticky=E)
ruFrame.grid(row=0, column=4, sticky=E)

# Main Loop
root.mainloop()