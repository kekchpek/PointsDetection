import numpy as np
import cv2
import threading


class Camera():

    def __init__(self, callback):
        if callback != None and not callable(callback):
            raise Exception("Callback should be callable")
        self.dataReceiveCallback = callback
        self.cap = cv2.VideoCapture(0)
        self.cancelHandleThread = False
        self.dataHandleThread = threading.Thread(target=self.__handleData)
        self.dataHandleThread.start()

    def __handleData(self):
        while not self.cancelHandleThread:
            ret, frame = self.cap.read()
            if ret and self.dataReceiveCallback != None:
                try:
                    self.dataReceiveCallback(frame)
                except Exception as inst:
                    print("error")
