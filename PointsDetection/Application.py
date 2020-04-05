import tkinter as tk
import traceback

import VideoModule as vm
import numpy as np
import cv2 as cv
from ContourMaskSettingsWidget import ContourMaskSettings
from HSVRangeDisplayWidget import  HSVRangeDisplay
import MyWidgets as mw




class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.__initCamera()
        self.__contourDetector = vm.MaskContoursDetector()
        self.__initVars()
        self.__createWidgets()

    def __initCamera(self):
        self.cam = vm.Camera(self.__receiveCameraData)

    def __initVars(self):
        # widgets
        self.__hueMinSeek = None
        self.__saturationMinSeek = None
        self.__valueMinSeek = None
        self.__hueMaxSeek = None
        self.__saturationMaxSeek = None
        self.__valueMaxSeek = None

        # vars
        self.__hueMinVar = tk.IntVar()
        self.__hueMinVar.trace_add('write', self.__changeLowMask)
        self.__saturationMinVar = tk.IntVar()
        self.__saturationMinVar.trace_add('write', self.__changeLowMask)
        self.__valueMinVar = tk.IntVar()
        self.__valueMinVar.trace_add('write', self.__changeLowMask)

        self.__hueMaxVar = tk.IntVar()
        self.__hueMaxVar.trace_add('write', self.__changeUpMask)
        self.__saturationMaxVar = tk.IntVar()
        self.__saturationMaxVar.trace_add('write', self.__changeUpMask)
        self.__valueMaxVar = tk.IntVar()
        self.__valueMaxVar.trace_add('write', self.__changeUpMask)

        self.__minContourVar = tk.IntVar()
        self.__minContourVar.trace_add('write', self.__changeContourAreaMin)

        self.__minContourRectVar = tk.IntVar()
        self.__minContourRectVar.trace_add('write', self.__changeContourRectAreaMin)

    def __createWidgets(self):
        self.__videoFrame = tk.Frame(master=self, width=600, height=400)
        self.__streamCanvas = mw.ImageCanvas(master=self.__videoFrame, width=300, height=200)
        self.__streamCanvas.pack_propagate(0)
        self.__streamCanvas.place(rely=0.25, relx=0.25, anchor='c')

        self.__streamPointsCanvas = mw.ImageCanvas(master=self.__videoFrame, width=300, height=200)
        self.__streamPointsCanvas.pack_propagate(0)
        self.__streamPointsCanvas.place(rely=0.25, relx=0.75, anchor='c')

        self.__streamContourCanvas = mw.ImageCanvas(master=self.__videoFrame, width=300, height=200)
        self.__streamContourCanvas.pack_propagate(0)
        self.__streamContourCanvas.place(rely=0.75, relx=0.25, anchor='c')

        self.__streamContourRectCanvas = mw.ImageCanvas(master=self.__videoFrame, width=300, height=200)
        self.__streamContourRectCanvas.pack_propagate(0)
        self.__streamContourRectCanvas.place(rely=0.75, relx=0.75, anchor='c')
        self.__videoFrame.pack(side=tk.LEFT)

        self.__hsvRangeDisplay = HSVRangeDisplay(self, self.__hueMinVar, self.__saturationMinVar, self.__valueMinVar,
                                                  self.__hueMaxVar, self.__saturationMaxVar, self.__valueMaxVar,
                                                  width=400, height=400)
        self.__hsvRangeDisplay.pack_propagate(0)
        self.__hsvRangeDisplay.pack(side=tk.LEFT)

        self.__colorSettingWidget = ContourMaskSettings(self, self.__hueMinVar, self.__saturationMinVar, self.__valueMinVar,
                                                  self.__hueMaxVar, self.__saturationMaxVar, self.__valueMaxVar,
                                                  self.__minContourVar, self.__minContourRectVar,
                                                  width=400, height=900)
        self.__colorSettingWidget.pack_propagate(0)
        self.__colorSettingWidget.pack(side=tk.LEFT)

    def __changeLowMask(self, *_):
        try:
            lowerMaskBorder = (self.__hueMinVar.get(), self.__saturationMinVar.get(), self.__valueMinVar.get())
            self.__contourDetector.setLowerMaskBorder(lowerMaskBorder)
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __changeUpMask(self, *_):
        try:
            upperMaskBorder = (self.__hueMaxVar.get(), self.__saturationMaxVar.get(), self.__valueMaxVar.get())
            self.__contourDetector.setUpperMaskBorder(upperMaskBorder)
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __changeContourAreaMin(self, *_):
        self.__contourDetector.setContourAreaMin(self.__minContourVar.get())

    def __changeContourRectAreaMin(self, *_):
        self.__contourDetector.setContourRectAreaMin(self.__minContourRectVar.get())

    def __receiveCameraData(self, data):
        data = cv.cvtColor(data, cv.COLOR_BGR2HSV)
        contourImg, contourRectImg, contours = self.__contourDetector.findContours(np.copy(data))
        contourImg = cv.cvtColor(contourImg, cv.COLOR_HSV2RGB)
        contourRectImg = cv.cvtColor(contourRectImg, cv.COLOR_HSV2RGB)
        centers = self.__getContoursCenters(contours)
        data = cv.cvtColor(data, cv.COLOR_HSV2RGB)
        circles = np.copy(data)
        for c in centers:
            circles = cv.circle(circles, c, 5, (0,255,0), 10)
        self.__streamCanvas.settleImageData(data)
        self.__streamContourCanvas.settleImageData(contourImg)
        self.__streamContourRectCanvas.settleImageData(contourRectImg)
        self.__streamPointsCanvas.settleImageData(circles)

    def __getContoursCenters(self, contours):
        centers = []
        for c in contours:
            M = cv.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centers.append((cx,cy))
        return centers


    def dispose(self):
        self.cam.dispose()
