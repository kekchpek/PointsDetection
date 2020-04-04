import colorsys
import tkinter as tk
import numpy as np
import cv2 as cv
from PIL import Image
from PIL import ImageTk

class ImageCanvas(tk.Canvas):

    SAVE_RATIO_MODE = 'save_ratio'
    FILL_MODE = 'fill'

    def __init__(self, master=None, cnf={}, **kw):
        super(ImageCanvas, self).__init__(master, cnf, **kw)
        self.__mode = self.SAVE_RATIO_MODE
        self.__rawImg = None
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.bind('<Configure>', self.__sizeChangedHandler)

    def __sizeChangedHandler(self, event=None):
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.__resizeImage()

    def __resizeImage(self):
        if(self.__rawImg == None):
            return
        imgWidth = self.__rawImg.width
        imgHeight = self.__rawImg.height
        newImgWidth = 0
        newImgHeight = 0
        if self.__mode == self.SAVE_RATIO_MODE:
            scale = min(self.width/imgWidth, self.height/imgHeight)
            newImgWidth = int(self.__rawImg.size[0]*scale)
            newImgHeight = int(self.__rawImg.size[1]*scale)
        if self.__mode == self.FILL_MODE:
            newImgWidth = self.width
            newImgHeight = self.height
        if newImgHeight != 0 and newImgWidth != 0:
            rawImg = self.__rawImg.resize((newImgWidth, newImgHeight), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(rawImg)
            self.create_image(self.width/2, self.height/2, anchor='c', image = img)
            self.__image = img

    def settleImageData(self, imgData):
        img = Image.fromarray(imgData)
        self.settlePILImage(img)

    def settlePILImage(self, image):
        self.__rawImg = image
        self.__resizeImage()

    def setMode(self, mode):
        if mode != self.SAVE_RATIO_MODE and mode != self.FILL_MODE:
            raise ValueError("Unknown mode")
        if mode == self.__mode:
            return
        self.__mode = mode
        self.__resizeImage()

    def getMode(self):
        return self.__mode

class GradientCanvas(tk.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, master = None, cnf = {}, color1="#ff0000", color2="#000000", **kw):
        super(GradientCanvas, self).__init__(master, cnf, **kw)
        self.__color1 = color1
        self.__color2 = color2
        self.bind("<Configure>", self.__drawGradient)

    def drawGradient(self, color1, color2):
        self.__color1 = color1
        self.__color2 = color2
        self.__drawGradient()

    def __drawGradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self.__color1)
        (r2,g2,b2) = self.winfo_rgb(self.__color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%04x%04x%04x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")

class SeekBar(tk.Frame):

    def __init__(self, master = None, **kw):
        self.__initDefaultSpecificConfig(**kw)
        kw = self.__updateSpecificConfig(**kw)
        self.__initParentWidget(master, **kw)
        self.__calculatePinPosRange()
        self.__createWidgets()
        self.bind('<Configure>', self.__onSizeChanged)
        self.bind('<B1-Motion>', self.__motion)
        self.bind('<Button-1>', self.__motion)

    def __initParentWidget(self, master, **kw):
        if 'width' not in kw:
            kw['width'] = 100
        if 'height' not in kw:
            kw['height'] = 20
        super().__init__(master=master, highlightthickness=0, **kw)

    def __initDefaultSpecificConfig(self, **kw):
        height = 20
        if 'height' in kw:
            height = kw.get('height')
        self.__minVal = 0
        self.__curVal = 0
        self.__useVariableValue = False
        self.__maxVal = 100
        self.__bgGradientColor1 = "#FFFFFF"
        self.__bgGradientColor2 = "#FFFFFF"
        self.__pinWidth = int(height)
        self.__pinHeight = int(height)
        self.__seekHeight = int(0.5 * height)
        self.__pinColor = '#75c1ff'
        self.__valueHandler = None
        self.__bgImage = None

    def __checkForAbnormalities(self, **kw):
        if 'seekBg' in kw and ('seekBg1' in kw or 'seekBg2' in kw):
            raise ValueError('kw can not contain "seekBg" and "seekBg1" or "seekBg2" at once')
        if 'seekBgImage' in kw and ('seekBg1' in kw or 'seekBg2' in kw):
            raise ValueError('kw can not contain "seekBgImage" and "seekBg1" or "seekBg2" at once')
        if 'seekBg' in kw and 'seekBgImage' in kw:
            raise ValueError('kw can not contain "seekBgImage" and "seekBgImage" at once')

    def __updateSpecificConfig(self, **kw):
        self.__checkForAbnormalities(**kw)
        if 'pinWidth' in kw:
            self.__pinWidth = kw.pop('pinWidth')
        if 'pinHeight' in kw:
            self.__pinHeight = kw.pop('pinHeight')
        if 'seekHeight' in kw:
            self.__seekHeight = kw.pop('seekHeight')
        if 'minVal' in kw:
            self.__minVal = kw.pop('minVal')
        if 'maxVal' in kw:
            self.__maxVal = kw.pop('maxVal')
        if 'pinColor' in kw:
            self.__pinColor = kw.pop('pinColor')
        if 'seekBg1' in kw:
            self.__bgGradientColor1 = kw.pop('seekBg1')
            self.__bgImage = None
        if 'seekBg2' in kw:
            self.__bgGradientColor2 = kw.pop('seekBg2')
            self.__bgImage = None
        if 'seekBg' in kw:
            bg = kw.pop('seekBg')
            self.__bgGradientColor1 = bg
            self.__bgGradientColor2 = bg
            self.__bgImage = None
        if 'seekBgImage' in kw:
            self.__bgImage = kw.pop('seekBgImage')
        if 'valueHandler' in kw:
            self.__valueHandler = kw.pop('valueHandler')

        return kw

    def __calculatePinPosRange(self):
        width = self.winfo_width()
        self.__minPinPos = int(self.__pinWidth * 0.5)
        self.__maxPinPos = width - int(self.__pinWidth * 0.5)

    def __updatePinPos(self):
        self.__curPinPos = self.__minPinPos + (self.__maxPinPos - self.__minPinPos) *(self.getValue() / (self.__maxVal - self.__minVal))
        self.__pin.place_configure(x = self.__curPinPos, rely=0.5, anchor = tk.CENTER)

    def __createWidgets(self):
        # Seek gradient bg
        self.__bgGradientCanvas = GradientCanvas(master=self, highlightthickness=0)
        self.__bgGradientCanvas.bind('<B1-Motion>', self.__motion)
        self.__bgGradientCanvas.bind('<Button-1>', self.__motion)
        self.__bgGradientCanvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.__bgGradientCanvas.drawGradient(self.__bgGradientColor1, self.__bgGradientColor2)

        # Seek image bg
        self.__bgImageCanvas = ImageCanvas(master=self, highlightthickness=0)
        self.__bgImageCanvas.setMode(ImageCanvas.FILL_MODE)
        self.__bgImageCanvas.bind('<B1-Motion>', self.__motion)
        self.__bgImageCanvas.bind('<Button-1>', self.__motion)
        if self.__bgImage != None:
            self.__bgImageCanvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.__bgImageCanvas.settlePILImage(self.__bgImage)

        # Pin
        self.__pin = tk.Canvas(master=self, width=self.__pinWidth, height =self.__pinHeight,
                               highlightthickness=0, bg = self.__pinColor)
        self.__pin.bind('<B1-Motion>', self.__motion)
        self.__pin.bind('<Button-1>', self.__motion)
        self.__updatePinPos()

    def __onSizeChanged(self, event = None):
        width = self.winfo_width()
        seekWidth = max(width - self.__pinWidth, 1)
        self.__bgGradientCanvas.configure(width = seekWidth, height=self.__seekHeight)
        self.__bgImageCanvas.configure(width = seekWidth, height=self.__seekHeight)
        self.__calculatePinPosRange()
        self.__updatePinPos()

    def __onConfigure(self):
        self.__pin.configure(width = self.__pinWidth, height=self.__pinHeight)

        if self.__bgImage != None:
            self.__bgImageCanvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.__bgImageCanvas.settlePILImage(self.__bgImage)
        else:
            self.__bgImageCanvas.place_forget()

        if self.__minVal >= self.__maxVal:
            raise ValueError('minVal >= maxVal')
        value = self.getValue()
        value = max(value, self.__minVal)
        value = min(value, self.__maxVal)
        self.setValue(value)

        self.__calculatePinPosRange()
        self.__updatePinPos()

        self.__bgGradientCanvas.drawGradient(self.__bgGradientColor1, self.__bgGradientColor2)

    def __motion(self, event = None):
        if event != None:
            x = event.x_root - self.winfo_rootx()
            seekX = x - self.__minPinPos
            value = int((seekX / (self.__maxPinPos - self.__minPinPos)) * (self.__maxVal - self.__minVal))
            value = max(value, self.__minVal)
            value = min(value, self.__maxVal)
            self.setValue(value)

    def configure(self, cnf=None, **kw):
        kw = self.__updateSpecificConfig(**kw)
        super().configure(**kw)
        self.__onConfigure()

    def setValue(self, value):
        if self.getValue() == value:
            return
        if value < self.__minVal or value > self.__maxVal:
            raise ValueError('Value is not in range [' + str(self.__minVal) + '; ' + str(self.__maxVal) + ']')
        if self.__useVariableValue:
            self.__curVal.set(value)
        else:
            self.__curVal = value
        if self.__valueHandler != None:
            self.__valueHandler(value)
        self.__updatePinPos()

    def getValue(self):
        if self.__useVariableValue:
            return self.__curVal.get()
        else:
            return self.__curVal

    def setVariable(self, variable):
        self.__useVariableValue = True
        self.__curVal = variable

    def resetVariable(self):
        self.__useVariableValue = False
        self.__curVal = self.__curVal.get()

class CanvasHS(tk.Frame):

    def __init__(self, master = None, cnf = {}, **kw):
        super().__init__(master = master, cnf = cnf, **kw)
        self.__initVars()
        self.__createWidgets()
        self.__loadImage()

    def __createWidgets(self):
        self.__imageCanvas = ImageCanvas(master = self)
        self.__imageCanvas.setMode(ImageCanvas.FILL_MODE)
        self.__imageCanvas.pack(fill=tk.BOTH)

    def __setImage(self, img):
        self.__imageCanvas.settleImageData(img)

    def __loadImage(self):
        # create HSV
        self.__HSVImage = np.full((256, 256, 3), 0)
        for i in range(256):
            for j in range(256):
                self.__HSVImage[j, i] = (i, j, 255)
        self.__HSVImage = self.__HSVImage.astype('uint8')
        # create RGB
        img = cv.cvtColor(self.__HSVImage, cv.COLOR_HSV2RGB)

        self.__setImage(img.astype('uint8'))

    def __initVars(self):
        self.__HSVImage = None
        self.__imageCanvas = None
        self.__value = 255
        self.__hueMin = 0
        self.__hueMax = 255
        self.__saturationMin = 0
        self.__saturationMax = 255

    def setHSVValue(self, value):
        if self.__value == value:
            return
        self.__value = value
        self.__HSVImage[:,:,2] = value
        self.__updateImage()

    def setHSBorders(self, minHue, maxHue, minSaturation, maxSaturetion):
        if minHue == self.__hueMin and maxHue == self.__hueMax and minSaturation == self.__saturationMin and maxSaturetion == self.__saturationMax:
            return
        self.__saturationMin = minSaturation
        self.__saturationMax = maxSaturetion
        self.__hueMin = minHue
        self.__hueMax = maxHue
        self.__updateImage()

    def __updateImage(self):
        borderColor = (0,0,0)
        if self.__value < 100:
            borderColor = (255,255,255)

        img = cv.cvtColor(self.__HSVImage, cv.COLOR_HSV2RGB)
        topHue = min(self.__hueMax + 1, 255)
        bottomHue = max(0, self.__hueMin - 1)
        topSaturation = min(self.__saturationMax + 1, 255)
        bottomsaturation = max(0, self.__saturationMin - 1)
        if self.__hueMax < 255:
            img[bottomsaturation:topSaturation,topHue] = borderColor
        if self.__hueMin > 0:
            img[bottomsaturation:topSaturation,bottomHue] = borderColor
        if self.__saturationMax < 255:
            img[topSaturation,bottomHue:topHue] = borderColor
        if self.__saturationMin > 0:
            img[bottomsaturation,bottomHue:topHue] = borderColor
        self.__setImage(img.astype('uint8'))

class CanvasHV(tk.Frame):

    def __init__(self, master = None, cnf = {}, **kw):
        super().__init__(master = master, cnf = cnf, **kw)
        self.__initVars()
        self.__createWidgets()
        self.__loadImage()

    def __createWidgets(self):
        self.__imageCanvas = ImageCanvas(master = self)
        self.__imageCanvas.setMode(ImageCanvas.FILL_MODE)
        self.__imageCanvas.pack(fill=tk.BOTH)

    def __setImage(self, img):
        self.__imageCanvas.settleImageData(img)

    def __loadImage(self):
        # create HSV
        self.__HSVImage = np.full((256, 256, 3), 0)
        for i in range(256):
            for j in range(256):
                self.__HSVImage[j, i] = (i, 255, j)
        self.__HSVImage = self.__HSVImage.astype('uint8')
        # create RGB
        img = cv.cvtColor(self.__HSVImage, cv.COLOR_HSV2RGB)

        self.__setImage(img.astype('uint8'))

    def __initVars(self):
        self.__HSVImage = None
        self.__imageCanvas = None
        self.__saturation = 255
        self.__hueMin = 0
        self.__hueMax = 255
        self.__valueMin = 0
        self.__valueMax = 255

    def setHSVSaturation(self, value):
        if self.__saturation == value:
            return
        self.__saturation = value
        self.__HSVImage[:,:,2] = value
        self.__updateImage()

    def setHSBorders(self, minHue, maxHue, minValue, maxValue):
        if minHue == self.__hueMin and maxHue == self.__hueMax and minSaturation == self.__valueMin and maxSaturetion == self.__ValueMax:
            return
        self.__valueMin = minValue
        self.__ValueMax = maxValue
        self.__hueMin = minHue
        self.__hueMax = maxHue
        self.__updateImage()

    def __updateImage(self):
        borderColor = (255,255,255)
        if self.__saturation < 100:
            borderColor = (0,0,0)

        img = cv.cvtColor(self.__HSVImage, cv.COLOR_HSV2RGB)
        topHue = min(self.__hueMax + 1, 255)
        bottomHue = max(0, self.__hueMin - 1)
        topSaturation = min(self.__valueMax + 1, 255)
        bottomsaturation = max(0, self.__valueMin - 1)
        if self.__hueMax < 255:
            img[bottomsaturation:topSaturation,topHue] = borderColor
        if self.__hueMin > 0:
            img[bottomsaturation:topSaturation,bottomHue] = borderColor
        if self.__valueMax < 255:
            img[topSaturation,bottomHue:topHue] = borderColor
        if self.__valueMin > 0:
            img[bottomsaturation,bottomHue:topHue] = borderColor
        self.__setImage(img.astype('uint8'))
