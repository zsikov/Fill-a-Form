from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
import random, math, string, textwrap

def createInstructionString():
    b= """Create or Update your signature manually or by uploading one in Update Signature. In Highlight and Form Fill you can use the signature or text input as the Field To use Form Fill upload a form and press search, a blue line goes through the first field found. If this is a field, input text. When finished or if it is not a field, press search again to continue. For Highlight Fill, highlight fields found and replace again replace them with text or your signature."""
    list = textwrap.wrap(b, 70)
    result = ""
    for letter in list:
        result = result + "\n" + letter.center(70)
    return result

def init(data):
    data.count = 0
    data.instructions = createInstructionString()
    data.error = None
    mostRecentMode = "Home Instructions"
    data.form = None
    data.formName = None
    data.imageStart = (5, 25)
    data.signature = None
    data.signatureName = None
    data.signatureList = []
    data.xrange, data.yrange = None, None
    data.fieldList = []
    data.fieldString = ""
    data.newFieldBounds = (3*data.width/4, data.height/2-75, 
                           data.width-50, data.height/2-25)
    data.fonts = {"Font A": (data.width-50, data.height/3-30, 20), 
                  "Font B": (data.width-50, data.height/3, 20),
                  "Font C": (data.width-50, data.height/3+30, 20)}
    data.fontList = ["Times", "Helvetica", "Courier"]
    data.font = "Times"
    data.hWidth = 20
    data.startPosn = None
    data.endPosn = None

def homeInit(data):
    data.buttons = {"Form Fill":(data.width/2, data.height/2, 20), 
                    "Highlight Fill":(data.width/2, data.height/2 + 40, 20),
                    "Update Signature":(data.width/2, data.height/2 + 80, 20),
                    "Home Instructions":(data.width/2, data.height/2 + 120, 20)}

def signatureInit(data):
    data.buttons = {"Back":(data.width-50, data.height-20, 20),
                    "Save":(data.width-50, 3*data.height/4, 20), 
                    "Upload":(data.width-50, 3*data.height/4+40, 20), 
                    "Home":(50, 20, 20), "Start":
                    (data.width/4, data.height/8, 20), "End":
                    (data.width/4 + 100, data.height/8, 20), "Start Over":
                    (data.width-50, 3*data.height/4-40, 20)}
    data.mousePosn = None
    data.signatureOn = False
    data.signatureBounds = (300, 200, 900, 500)
    
def highlightInit(data):
    data.buttons = {"Home":(50, 20, 20),
                    "Use Signature":(data.width-50, data.height-50, 20),
                    "Update Signature":(data.width-50, 
                    data.height-20, 20), "Input Finished":
                    (data.width-50, data.height/2, 20), "Upload": 
                    (3*data.width/4, 3*data.height/4, 20), "Undo Field": 
                    (data.width-50, 50, 20), "Save": (data.width-50, 100, 20)}
    data.highlight={"leftPosn": None, "rect": None, "startPosn": None, 
                    "endPosn":None}

def fillInit(data):
    data.buttons = {"Home":(50, 20, 20), "Search": (data.width-50, 50, 20),
                    "Use Signature":(data.width-50, data.height-100, 20),
                    "Update Signature":(data.width-50, 
                    data.height-10, 20), "Input Finished":
                    (data.width-50, data.height/2, 20), "Upload": 
                    (3*data.width/4, 3*data.height/4, 20), "Save": 
                    (data.width-50, 100, 20)}
    data.center = None

def resize(image, areaWidth, areaHeight):
    width = image.width()
    height = image.height()
    newImage = image.zoom(max(1, round(areaWidth/(2*width))), 
                              max(1, round(areaHeight/(2*height))))
    image = newImage.subsample(max(1, round((2*width)/areaWidth)), 
                                   max(1, round((2*height)/areaHeight)))
    return image

# lines 43 and 44 are from stack overflow 
def upload(root, data):
    path = filedialog.askopenfilename(filetypes=(
                ("portable network graphics", "*.png"), ("All files", "*.*")))
    for form in path.split("/"):
        if "." in form:
            # data.form = "%s" % (form)
            if data.mode == "signature":
                data.signatureName = form
                data.signature = PhotoImage(file=form)
            else:
                data.formName = form
                data.form = PhotoImage(file=form)
                data.form = resize(data.form, data.width, data.height)

def buttonPressed(x, y, buttons):
    for button in buttons:
        (x1, y1, buttonSize) = buttons[button]
        halfButtonLen = len(button)*buttonSize/2
        if (x1-halfButtonLen<=x<=x1+halfButtonLen and 
            y1-buttonSize/2<=y<=y1+buttonSize/2):
            return button
    return None

def modeInit(data):
    if data.mode == "fill":
        fillInit(data)
    elif data.mode == "highlight":
        highlightInit(data)
    elif data.mode == "signature":
        signatureInit(data)
    else:
        homeInit(data)

def instructionMousePressed(event, data):
    data.mode = "home"
    data.mostRecentMode = "Home Instructions"
    homeInit(data)

def instructionKeyPressed(event, data):
    data.mode = "home"
    data.mostRecentMode = "Home Instructions"
    homeInit(data)

def instructionRedrawAll(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill="white")
    canvas.create_text(data.width/2, data.height/4, font="Times 30",
                       text="Welcome to\nFill A Form")
    canvas.create_text(data.width/2, 3*data.height/8, font="TImes 25",
                       text="Instructions:")
    canvas.create_text(data.width/2, 3*data.height/8 + 50, font="Times 20",
                text="Press the screen or any button to go to the Home Page")
    canvas.create_text(data.width/2, data.height/2, font="Times 20", anchor=N,
         text=data.instructions)

def homeMousePressed(event, data):
    pressed = buttonPressed(event.x, event.y, data.buttons)
    if pressed != None:
        data.mostRecentMode = data.mode
        if pressed == "Form Fill":
            data.mode = "fill"
        elif pressed == "Highlight Fill":
            data.mode = "highlight"
        elif pressed == "Update Signature":
            data.mode = "signature"
        elif pressed == "Home Instructions":
            data.mode = "Home Instructions"
    modeInit(data)

def drawButtons(canvas, buttons, data):
    for button in buttons:
        (x, y, buttonSize) = buttons[button]
        if x>3*data.width/4:
            canvas.create_text(x, y, font="Times %d" %
                          (buttonSize), text=button, anchor=E)
        else:
            canvas.create_text(x, y, font="Times %d" %
                          (buttonSize), text=button)

def homeRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="white")
    canvas.create_image(data.width/2, data.height/2, image=data.background)
    canvas.create_text(data.width/2, data.height/4, font="Times 30",
                       text="Welcome to\nFill A Form")
    drawButtons(canvas, data.buttons, data)

def homeKeyPressed(event, data):
    pass
def homeTimerFired(data):
    pass

def saveSignature(root, event, data):
    (x1, y1, x2, y2) = data.signatureBounds
    image = Image.new("RGB", [x2-x1, y2-y1], (255,255,255))
    draw = ImageDraw.Draw(image)
    for pixel in range(len(data.signatureList)-1):
        (x0,y0) = data.signatureList[pixel]
        (x, y) = data.signatureList[pixel+1]
        draw.line((x0-x1, y0-y1) + (x-x1, y-y1), fill=0)
    image.save(data.signatureName, bob="PNG")
    data.signature = PhotoImage(file=data.signatureName)

def signatureMousePressed(root, event, data):
    pressed = buttonPressed(event.x, event.y, data.buttons)
    if pressed == "Save" and len(data.signatureList) > 0:
        saveSignature(root, event, data)
        data.signatureOn = False
    if pressed == "Upload":
        upload(root, data)
        data.signatureOn = False
    elif pressed == "Back":
        (data.mode, data.mostRecentMode) = (data.mostRecentMode, data.mode)
        modeInit(data)
        data.signatureOn = False
    elif pressed == "Home":
        (data.mode, data.mostRecentMode) = ("home", data.mode)
        modeInit(data)
        data.signatureOn = False
    elif pressed == "Start":
        data.signatureOn = True
    elif pressed == "End":
        data.signatureOn = False
    elif pressed == "Start Over":
        data.signature = None
        data.signatureName = None
        data.signatureOn = False
        data.signatureList = []

def mouseInBounds(x, y, bounds):
    (x1, y1, x2, y2) = bounds
    if x1 < x < x2 and y1 < y < y2:
        return True
    return False

def signatureMouseMotion(event, data):
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)    
    data.mousePosn = (event.x, event.y)
    if data.signatureOn and mouseInBounds(event.x, event.y, 
                                          data.signatureBounds):
        if len(data.signatureList) == 0:
            data.signatureName = "Free Draw.png"
        data.signatureList += [data.mousePosn]

def signatureKeyPressed(event, data):
    pass
def signatureTimerFired(data):
    pass

def drawSignature(canvas, data):
    (x1, y1, x2, y2) = data.signatureBounds
    if data.signature == None:
        canvas.create_rectangle(data.signatureBounds, fill="white", 
                                outline="Black")
        if data.signatureList != None:
            for pixel in range(len(data.signatureList)-1):
                canvas.create_line(data.signatureList[pixel], 
                    data.signatureList[pixel+1], fill="black", width="1")
    else:
        canvas.create_image(x1, y1, image=data.signature, anchor=NW)

def signatureRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="white")
    drawButtons(canvas, data.buttons, data)
    drawSignature(canvas, data)

def fontPressed(pressed, data):
    if pressed == "Font A":
        data.font = data.fontList[0]
    elif pressed == "Font B":
        data.font = data.fontList[1]
    elif pressed == "Font C":
        data.font = data.fontList[2]

def updateFields(data, pressed):
    if pressed == "Use Signature":
        fieldName = data.signatureName
        newField = data.signature
    elif pressed == "Input Finished":
        (x1, y1, x2, y2) = data.newFieldBounds
        xChange = round(x2-x1)
        yChange = round(y2-y1)
        image = Image.new("RGB", [len(data.fieldString)*10, 20], (255,255,255))
        draw = ImageDraw.Draw(image)
        fnt= ImageFont.truetype("arial.ttf")
        draw.text((20, 10), text=data.fieldString[:27], font=fnt, fill="#000000")
        fieldName = "New Field %d.png" % (random.randint(1,10**10))
        image.save(fieldName, bob="PNG")
    if data.mode == "highlight":
        (x0, y0) = data.highlight["startPosn"]
        xCenter = x0+data.adj/2
        yCenter =y0+data.opp/2
        (width, height) = (data.hyp, data.hWidth)
        if data.opp and data.adj:
            rotation = math.atan((data.opp/data.adj)*180/math.pi)
        else: rotation = 0
    else:
        (width, height) = data.size
        (xCenter, yCenter) = data.center
        rotation = 0
    im = Image.open(fieldName)
    im2 = im.rotate(rotation)   
    im2.save(fieldName)
    newField = PhotoImage(file=fieldName)
    if pressed == "Use Signature":
        newField = resize(newField, width, height)
    data.fieldList +=[(xCenter, yCenter, newField, fieldName)]

def highlightMousePressed(root, event, data):
    pressed = buttonPressed(event.x, event.y, data.buttons)
    if pressed == None:
        pressed = buttonPressed(event.x, event.y, data.fonts)
    if pressed != None:
        if pressed == "Home":
            (data.mode, data.mostRecentMode) = ("home", data.mode)
            modeInit(data)
        elif (pressed == "Use Signature" and data.form != None 
             and data.highlight["startPosn"] != None):
            if data.signature == None:
                data.error = "No Signature Exists, Update Signature!!"
            else:
                updateFields(data, pressed)
        elif pressed == "Update Signature":
            (data.mode, data.mostRecentMode) = ("signature", data.mode)
            modeInit(data)
        elif (pressed == "Input Finished" and data.form != None 
              and data.highlight["startPosn"] != None): 
            if len(data.fieldString) == 0:
                data.error = """You must add text to finish input
Continue Searching if this is not a field"""
            else:
                updateFields(data, pressed)
                data.fieldString = ""
                data.error = None
        elif pressed == "Upload":
            upload(root, data)
        elif pressed == "Undo Field" and len(data.fieldList) > 0:
            data.fieldList.pop(-1)
        elif (pressed == "Save" and len(data.fieldList) > 0 and 
              data.form != None):
            saveForm(data)
        elif pressed in data.fonts:
            fontPressed(pressed, data)
    data.highlight["startPosn"] = None
    if data.form != None:
        img = Image.open(data.formName)
        pix = img.load()
        image_size= img.size
        data.xrange = image_size[0]
        data.yrange = image_size[1]
        (x,y) = data.imageStart
    if data.form != None and mouseInBounds(event.x, event.y, (x, y, 
                                           x+data.xrange, y+data.yrange)):
        ctrl  = ((event.state & 0x0004) != 0)
        shift = ((event.state & 0x0001) != 0)
        data.highlight['startPosn'] = (event.x, event.y)
        data.highlight["endPosn"] = None   
        data.highlight["leftPosn"] = (event.x, event.y) 

# From course notes on mouse motion
def leftMouseMoved(event, data):
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    data.highlight["leftPosn"] = (event.x, event.y)

# From course notes on mouse motion
def leftMouseReleased(event, data):
    (x,y) = data.imageStart
    if data.xrange != None and data.yrange != None and mouseInBounds(event.x,
                                     event.y, (x, y, data.xrange, data.yrange)):
        ctrl  = ((event.state & 0x0004) != 0)
        shift = ((event.state & 0x0001) != 0)
        data.highlight['endPosn'] = (event.x, event.y)   
        data.highlight["leftPosn"] = (event.x, event.y)
        rectCoordinates(data)

def rectCoordinates(data):
    if data.highlight["startPosn"] != None:
        (x0, y0) = data.highlight["startPosn"]
    if data.highlight["endPosn"] != None:
        (x1, y1) = data.highlight["endPosn"]
    if data.highlight["startPosn"] and data.highlight["endPosn"]:
        data.opp = (y1-y0)
        data.adj = (x1-x0)
    else:
        data.opp, data.adj = None, None
    hWidth = data.hWidth
    data.hyp = (data.opp**2 + data.adj**2)**.5
    if data.opp and data.adj: # opp and adj are not 0
        xChange = data.opp/data.hyp * 1/2*hWidth
        yChange = data.adj/data.hyp * 1/2*hWidth
        data.highlight["rect"] = ((x0-xChange, y0+yChange), (x0+xChange, 
                                   y0-yChange), (x1+xChange, y1-yChange), 
                                  (x1-xChange, y1+yChange))
    elif data.adj:
        data.highlight["rect"] = ((x0, y0-1/2*hWidth), (x0,y0+1/2*hWidth), 
                               (x1, y1+1/2*hWidth), (x1, y1-1/2*hWidth))
    elif data.opp:
        data.highlight["rect"] = ((x0-1/2*hWidth, y0), (x0+1/2*hWidth,y0), 
                               (x1+1/2*hWidth, y1), (x1-1/2*hWidth, y1))
    else:
        data.highlight["rect"] = None

def highlightKeyPressed(event, data):
    if event.keysym in string.printable:
        data.fieldString = data.fieldString + "%s" % (event.keysym)
        if len(data.fieldString) > 26:
            data.error = "Your text is too long!!!"
    elif event.keysym == "BackSpace":
        data.fieldString = data.fieldString[:-1]
    elif event.keysym == "space":
        data.fieldString = data.fieldString + " "

def highlightTimerFired(data):
    pass

def drawFields(canvas, data):
    for field in range(len(data.fieldList)):
        (x,y, image, fieldName) = data.fieldList[field]
        canvas.create_image(x, y, image=image)

def highlightRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="white")
    if data.form != None:
        canvas.create_image(data.imageStart, image=data.form, anchor=NW) # PhotoImage(data.form)
    drawFields(canvas, data)
    if data.highlight["rect"] != None:
        canvas.create_polygon(data.highlight["rect"], fill="blue")
    canvas.create_rectangle(data.newFieldBounds, outline='black')
    if 0 <= len(data.fieldString) < 25:
        canvas.create_text(3*data.width/4 + 5, data.height/2-67.5, 
                           text=data.fieldString, fill="black", 
                           font="%s 14" % (data.font), anchor=NW)
    else:
        canvas.create_text(3*data.width/4 + 5, data.height/2 - 67.5,
                           text=data.fieldString[:26], fill="black", 
                           font="%s 14" % (data.font), anchor=NW)
        canvas.create_text(3*data.width/4, data.height/2 - 95, 
                           text="Your text is too long!!!", fill="black",
                           font="Times 14", anchor=NW)
    drawButtons(canvas, data.fonts, data)
    drawButtons(canvas, data.buttons, data)

def saveForm(data):
    image = Image.open(data.formName)
    (x0, y0) = data.imageStart
    (x1, y1) = (x0 + data.form.width(), y0 + data.form.height())
    for fieldTuple in data.fieldList:
        (xCenter, yCenter, field, fieldName) = fieldTuple
        im2 = Image.open(fieldName)
        pix = im2.load()
        width = field.width()
        height = field.height()
        (upperX, upperY) = (round(xCenter - width//2 - x0), 
                            round(yCenter - height - y0))
        # (lowerX, lowerY) = (xCenter + width/2 - x0, yCenter - y0)
        for x in range(width):
            for y in range(height):
                image.putpixel((upperX + x, upperY + y), pix[x, y])
    data.formName =data.formName[:-4] + "%d.png" % (random.randint(1, 10**10))
    image.save(data.formName)
    data.fieldList = []
    data.form = PhotoImage(file=data.formName)

def search(data, point=(0,0)):
    img = Image.open(data.formName)
    pix = img.load()
    (i, j) = point
    image_size= img.size
    xrange = image_size[0] # set the x-range of the image from the image size.
    yrange = image_size[1]
    while(j < yrange):
        count = 0
        while (i < xrange):
            value = pix[i,j]
            if sum(value) < 500:
                if count == 0: data.startPosn = (i,j)
                count += 1
            else:
                if count >= 10:
                    data.endPosn = (i,j)
                    (i0,j0) = data.startPosn
                    data.size = (i-i0, data.hWidth)
                    data.center = (i0+(i-i0)/2, j0)
                    return None
                count = 0
            i += 1
        i = 0
        j +=1
    data.endPosn = (0,0)
    data.startPosn = None

def fillMousePressed(canvas, root, event, data):
    pressed = buttonPressed(event.x, event.y, data.buttons)
    if pressed == None:
        pressed = buttonPressed(event.x, event.y, data.fonts)
    if pressed != None:
        if pressed == "Home":
            (data.mode, data.mostRecentMode) = ("home", data.mode)
            modeInit(data)
        elif pressed == "Search" and data.form != None:
            if data.endPosn != None:
                search(data, data.endPosn)
            else:
                search(data)
        elif (pressed == "Use Signature"and data.form != None 
             and data.endPosn != None):
            if data.signature == None:
                data.error = "No Signature Exists, Update Signature!!"
            else:
                updateFields(data, pressed)
        elif pressed == "Update Signature":
            (data.mode, data.mostRecentMode) = ("signature", data.mode)
            modeInit(data)
        elif (pressed == "Input Finished" and data.form != None 
              and data.endPosn != None):
            if len(data.fieldString) == 0:
                data.error = """You must add text to finish input
Continue Searching if this is not a field"""
            else:
                updateFields(data, pressed)
                data.fieldString = ""
                data.error = None
        elif pressed == "Upload":
            upload(root, data)
        elif pressed == "Undo Field" and len(data.fieldList) > 0:
            data.fieldList.pop(-1)
        elif (pressed == "Save" and len(data.fieldList) > 0 and 
             data.form != None):
            saveForm(data)
        elif pressed in data.fonts:
            fontPressed(pressed, data)

def fillKeyPressed(event, data):
    if event.keysym in string.printable:
        data.fieldString = data.fieldString + "%s" % (event.keysym)
        if len(data.fieldString) > 26:
            data.error = "Your text is too long!!!"
    elif event.keysym == "BackSpace":
        data.fieldString = data.fieldString[:-1]
    elif event.keysym == "space":
        data.fieldString = data.fieldString + " "

def fillTimerFired(data):
    if data.error != None:
        data.count += 1
        if data.count > 10:
            data.error = None
            data.count = 0

def fillRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="white")
    if data.form != None:
        canvas.create_image(data.imageStart, image=data.form, anchor=NW) # PhotoImage(data.form)
    if data.startPosn != None and data.endPosn != None:
        ((x0, y0), (x1, y1), (x2, y2)) = (data.imageStart, data.startPosn, data.endPosn)
        canvas.create_line(x0+x1, y0+y1, x0+x2, y0+y2, fill="blue", width=5)
    drawFields(canvas, data)
    canvas.create_rectangle(data.newFieldBounds, outline='black')
    if 0 <= len(data.fieldString) < 25:
        canvas.create_text(3*data.width/4 + 5, data.height/2-67.5, 
                           text=data.fieldString, fill="black", 
                           font="%s 14" % (data.font), anchor=NW)
    else:
        canvas.create_text(3*data.width/4 + 5, data.height/2 - 67.5,
                           text=data.fieldString[:26], fill="black", 
                           font="%s 14" % (data.font), anchor=NW)
    if data.error != None:
        canvas.create_text(3*data.width/4, data.height/2, text=data.error,
                           fill="black", font="Times 14", anchor=NW)
    drawButtons(canvas, data.fonts, data)
    drawButtons(canvas, data.buttons, data)

####################################
# Modified Run Function from Animation Course Notes
####################################

def run():
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        if data.mode=="highlight":
            highlightRedrawAll(canvas, data)
        elif data.mode == "signature":
            signatureRedrawAll(canvas, data)
        elif data.mode == "fill":
            fillRedrawAll(canvas, data)
        elif data.mode == "Home Instructions":
            instructionRedrawAll(canvas, data)
        else:
            homeRedrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(root, event, canvas, data):
        if data.mode=="highlight":
            highlightMousePressed(root, event, data)
        elif data.mode == "signature":
            signatureMousePressed(root, event, data)
        elif data.mode == "fill":
            fillMousePressed(canvas, root, event, data)
        elif data.mode == "Home Instructions":
            instructionMousePressed(event, data)
        else:
            homeMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        if data.mode=="highlight":
            highlightKeyPressed(event, data)
        elif data.mode == "signature":
            signatureKeyPressed(event, data)
        elif data.mode == "fill":
            fillKeyPressed(event, data)
        elif data.mode == "Home Instructions":
            instructionKeyPressed(event, data)
        else:
            homeKeyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        if data.mode=="highlight":
            highlightTimerFired(data)
        elif data.mode == "signature":
            signatureTimerFired(data)
        elif data.mode == "fill":
            fillTimerFired(data)
        else:
            fillTimerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    def leftMouseMovedWrapper(event, data):
        if data.mode == "highlight":
            leftMouseMoved(event, data)
    def leftMouseReleasedWrapper(event, data):
        if data.mode == "highlight":
            leftMouseReleased(event, data)
    def mouseMotionWrapper(event, data):
        if data.mode == "signature":
            signatureMouseMotion(event, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = 1200
    data.height = 700
    data.mode = "Home Instructions"
    data.timerDelay = 1 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    data.background = PhotoImage(file="212-free-retro-line-background-vector-art.png")
    # root.one=data.background
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(root, event, canvas, data))
    canvas.bind("<B1-Motion>",lambda event: leftMouseMovedWrapper(event, data))
    root.bind("<B1-ButtonRelease>", lambda event:
                                leftMouseReleasedWrapper(event, data))
    root.bind("<Motion>", lambda event: mouseMotionWrapper(event, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()