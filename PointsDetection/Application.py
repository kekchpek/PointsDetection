import tkinter as tk
import numpy as np
import VideoModule as vm
import threading
import time
from PIL import ImageTk
from PIL import Image

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.__create_widgets()
        self.__initCamera()
        #t = threading.Thread(target = self.__testVideo)
        #t.start()

    def __initCamera(self):
        self.cam = vm.Camera(self.__receiveCameraData)

    def __create_widgets(self):
        randomArray = np.zeros((255,255, 3), dtype='uint8')
        byteArray = randomArray.astype(np.uint8)
        self.__streamImg = self.__byteArrayToImage(byteArray)
        self.__streamCanvas = tk.Canvas(width = 900, height = 600)
        self.__streamCanvas.create_image(0,0, anchor='nw', image = self.__streamImg)
        self.__streamCanvas.pack()

    def __receiveCameraData(self, data):
        img = self.__byteArrayToImage(data)
        self.__streamCanvas.create_image(0,0, anchor='nw', image = img)
        self.__streamImg = img

    def dispose(self):
        self.cam.dispose()

    @staticmethod
    def __byteArrayToImage(byteArray):
        img = ImageTk.PhotoImage(Image.fromarray(byteArray))
        return img

