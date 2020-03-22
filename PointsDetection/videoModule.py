import numpy as np
import cv2
import threading


class Camera():

    def __init__(self, callback):
        if callback != None and not callable(callback):
            raise Exception("Callback should be callable")
        self.__dataReceiveCallback = callback
        self.__cap = cv2.VideoCapture(0)
        self.__cancelHandleThread = threading.Event()
        self.__dataHandleThread = threading.Thread(name='cameraThread', target=self.__handleData)
        self.__dataHandleThread.daemon = True
        self.__dataHandleThread.start()

    def __isStopped(self):
        return self.__cancelHandleThread.set()

    def __stop(self):
        self.__cancelHandleThread.isSet()

    def __handleData(self):
        while True:
            if self.__isStopped():
                return
            ret, frame = self.__cap.read()
            if ret and self.__dataReceiveCallback != None:
                try:
                    self.__dataReceiveCallback(frame)
                except Exception as inst:
                    print("error")
        print('end of cycle')

    
    def dispose(self):
        self.__stop()
        self.__cap.release()
