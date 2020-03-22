import tkinter as tk

import VideoModule as vm
import numpy as np
import MyWidgets as mw


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.__create_widgets()
        self.__initCamera()

    def __initCamera(self):
        self.cam = vm.Camera(self.__receiveCameraData)

    def __create_widgets(self):
        randomArray = np.random.rand(255,255, 3) * 255
        byteArray = randomArray.astype(np.uint8)
        self.__streamCanvas = mw.ImageCanvas(width = 900, height = 600)
        self.__streamCanvas.settleImageData(byteArray)
        self.__streamCanvas.pack()

    def __receiveCameraData(self, data):
        self.__streamCanvas.settleImageData(data)

    def dispose(self):
        self.cam.dispose()

