import tkinter as tk
import traceback

import VideoModule as vm
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

    def __createWidgets(self):
        self.__streamCanvas = mw.ImageCanvas(master=self, width=600, height=400)
        self.__streamCanvas.pack(side=tk.LEFT)

        self.__hsvRangeDisplay = HSVRangeDisplay(self, self.__hueMinVar, self.__saturationMinVar, self.__valueMinVar,
                                                  self.__hueMaxVar, self.__saturationMaxVar, self.__valueMaxVar,
                                                  width=400, height=400)
        self.__hsvRangeDisplay.pack_propagate(0)
        self.__hsvRangeDisplay.pack(side=tk.LEFT)

        self.__colorSettingWidget = ContourMaskSettings(self, self.__hueMinVar, self.__saturationMinVar, self.__valueMinVar,
                                                  self.__hueMaxVar, self.__saturationMaxVar, self.__valueMaxVar,
                                                  self.__minContourVar,
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

    def __receiveCameraData(self, data):
        data = cv.cvtColor(data, cv.COLOR_BGR2HSV)
        data, contours = self.__contourDetector.findContours(data)
        data = cv.cvtColor(data, cv.COLOR_HSV2RGB)
        self.__streamCanvas.settleImageData(data)

    def dispose(self):
        self.cam.dispose()
