import threading
import traceback

import numpy as np
import cv2


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
                    print(type(inst))
                    print(inst.args)
                    print(inst)
                    traceback.print_exc()
                    return

    def dispose(self):
        self.__stop()
        self.__cap.release()

class MaskContoursDetector():

    def __init__(self, lowerMaskBorder = (0, 0, 0), upperMaskBorder = (255, 255, 255), contourAreaMin = 0):
        self.__lowerMaskBorder = lowerMaskBorder
        self.__upperMaskBoreder = upperMaskBorder
        self.__contourAreaMin = contourAreaMin

    def getLowerMaskBorder(self):
        return self.__lowerMaskBorder

    def getUpperMaskBorder(self):
        return self.__upperMaskBoreder

    def setLowerMaskBorder(self, hsvTuple):
        self.__lowerMaskBorder = hsvTuple

    def setUpperMaskBorder(self, hsvTuple):
        self.__upperMaskBoreder = hsvTuple

    def setContourAreaMin(self, value):
        self.__contourAreaMin = value

    def getcontourAreaMin(self):
        return self.__contourAreaMin

    def findContours(self, hsvData):
        mask = cv2.inRange(hsvData, self.__lowerMaskBorder, self.__upperMaskBoreder)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c)>self.__contourAreaMin]
        frame = cv2.drawContours(hsvData, contours, -1, (0,255,255), thickness=5)
        return frame, contours
