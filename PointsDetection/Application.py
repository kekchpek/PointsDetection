import tkinter as tk

import VideoModule as vm
import numpy as np
import cv2 as cv
import MyWidgets as mw




class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.__create_widgets()
        self.__initCamera()
        self.__contourDetector = vm.MaskContoursDetector()

    def __initCamera(self):
        self.cam = vm.Camera(self.__receiveCameraData)

    def __create_widgets(self):
        self.__streamCanvas = mw.ImageCanvas(master=self, width=600, height=400)
        self.__streamCanvas.pack(side=tk.LEFT)
        self.__initContourDetectorSettingsWidgets()

    def __initContourDetectorSettingsWidgets(self):
        self.__colorSettingsControl = tk.Canvas(master=self, width=600, height=600, bg="blue")
        self.__colorSettingsControl.pack_propagate(0)

        # Lower border
        self.__lowerMaskLabel = tk.Label(master = self.__colorSettingsControl, text="Lower mask border")
        self.__lowerMaskLabel.pack(fill=tk.X, side=tk.TOP)

        self.__hueMinSeek = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                     from_=0, to=255, label="Hue", command=self.__changeLowMask)
        self.__hueMinSeek.set(94)
        self.__hueMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        self.__saturationMinSeek = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                            from_=0, to=255, label="Saturtation", command=self.__changeLowMask)
        self.__saturationMinSeek.set(43)
        self.__saturationMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        self.__valueMinSeek = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                       from_=0, to=255, label="Value", command=self.__changeLowMask)
        self.__valueMinSeek.set(23)
        self.__valueMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        # Delimiter
        self.__maskSettingsDelimiter = tk.Frame(master = self.__colorSettingsControl, height=20)
        self.__maskSettingsDelimiter.pack(fill=tk.X, side=tk.TOP)

        # Upper border
        self.__upperMaskLabel = tk.Label(master = self.__colorSettingsControl, text="Upper mask border")
        self.__upperMaskLabel.pack(fill=tk.X, side=tk.TOP)

        self.__hueMaxSeek = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                     from_=0, to=255, label="Hue", command=self.__changeUpMask)
        self.__hueMaxSeek.set(153)
        self.__hueMaxSeek.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        self.__saturationMaxSeek = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                            from_=0, to=255, label="Saturtation", command=self.__changeUpMask)
        self.__saturationMaxSeek.set(255)
        self.__saturationMaxSeek.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        self.__valueMaxSeek = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                       from_=0, to=255, label="Value", command=self.__changeUpMask)
        self.__valueMaxSeek.set(255)
        self.__valueMaxSeek.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        # Delimiter
        self.__maskSettingsDelimiter2 = tk.Frame(master = self.__colorSettingsControl, height=20)
        self.__maskSettingsDelimiter2.pack(fill=tk.X, side=tk.TOP)

        # Contour area
        self.__minContourAreaLabel = tk.Label(master = self.__colorSettingsControl, text="Contour area")
        self.__minContourAreaLabel.pack(fill=tk.X, side=tk.TOP)

        self.__contourAreaMin = tk.Scale(master=self.__colorSettingsControl, orient=tk.HORIZONTAL, bg="red",
                                     from_=0, to=1000, label="Min contour area", command=self.__changeContourAreaMin)
        self.__contourAreaMin.set(200)
        self.__contourAreaMin.pack(fill=tk.X, side=tk.TOP, pady=(5,5), padx=20)

        self.__colorSettingsControl.pack(side=tk.TOP)

    def __changeLowMask(self, _):
        lowerMaskBorder = (self.__hueMinSeek.get(), self.__saturationMinSeek.get(), self.__valueMinSeek.get())
        self.__contourDetector.setLowerMaskBorder(lowerMaskBorder)

    def __changeUpMask(self, _):
        upperMaskBorder = (self.__hueMaxSeek.get(), self.__saturationMaxSeek.get(), self.__valueMaxSeek.get())
        self.__contourDetector.setUpperMaskBorder(upperMaskBorder)

    def __changeContourAreaMin(self, value):
        self.__contourDetector.setContourAreaMin(int(value))

    def __receiveCameraData(self, data):
        data = cv.cvtColor(data, cv.COLOR_BGR2HSV)
        data, contours = self.__contourDetector.findContours(data)
        data = cv.cvtColor(data, cv.COLOR_HSV2RGB)
        self.__streamCanvas.settleImageData(data)

    def dispose(self):
        self.cam.dispose()
