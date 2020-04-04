import tkinter as tk
import cv2 as cv
import traceback
import numpy as np
import MyWidgets as mw

import PIL


class ContourMaskSettings(tk.Frame):

    def __init__(self, master, hueMinVar, saturationMinVar, valueMinVar, hueMaxVar,
                 saturationMaxVar, valueMaxVar, contourMinVar, **kw):
        super().__init__(master=master, cnf={}, **kw)
        self.__hueMinVar = hueMinVar
        self.__saturationMinVar = saturationMinVar
        self.__valueMinVar = valueMinVar
        self.__hueMaxVar = hueMaxVar
        self.__saturationMaxVar = saturationMaxVar
        self.__valueMaxVar = valueMaxVar
        self.__contourMinVar = contourMinVar

        self.__initContourDetectorSettingsWidgets()

        self.__hueMinVar.trace_add('write', self.__onHueMinChanged)
        self.__saturationMinVar.trace_add('write', self.__onSaturationMinChanged)
        self.__valueMinVar.trace_add('write', self.__onValueMinChanged)
        self.__hueMaxVar.trace_add('write', self.__onHueMaxChanged)
        self.__saturationMaxVar.trace_add('write', self.__onSaturationMaxChanged)
        self.__valueMaxVar.trace_add('write', self.__onValueMaxChanged)
        self.__contourMinVar.trace_add('write', self.__onContourMinChanged)

    @staticmethod
    def __hsvToRgb(src):
        arr = np.zeros((1,1,3), dtype='uint8')
        arr[0,0] = src
        res = cv.cvtColor(arr, cv.COLOR_HSV2RGB)
        return tuple(res[0,0])

    def __updateMinSaturationColor(self):
            saturationHsv1 = (self.__hueMinVar.get(), 0, 255)
            saturationHsv2 = (self.__hueMinVar.get(), 255, 255)
            saturationRgb1 = self.__hsvToRgb(saturationHsv1)
            saturationRgb2 = self.__hsvToRgb(saturationHsv2)
            saturationColor1 = "#%02x%02x%02x" % saturationRgb1
            saturationColor2 = "#%02x%02x%02x" % saturationRgb2
            if self.__saturationMinSeek != None:
                self.__saturationMinSeek.configure(seekBg1 = saturationColor1, seekBg2 = saturationColor2)

    def __updateMinValueColor(self):
            valueHsv1 = (self.__hueMinVar.get(), self.__saturationMinVar.get(), 0)
            valueHsv2 = (self.__hueMinVar.get(), self.__saturationMinVar.get(), 255)
            valueRgb1 = self.__hsvToRgb(valueHsv1)
            valueRgb2 = self.__hsvToRgb(valueHsv2)
            valueColor1 = "#%02x%02x%02x" % valueRgb1
            valueColor2 = "#%02x%02x%02x" % valueRgb2
            if(self.__valueMinSeek != None):
                self.__valueMinSeek.configure(seekBg1 = valueColor1, seekBg2 = valueColor2)

    def __updateMaxSaturationColor(self):
            saturationHsv1 = (self.__hueMaxVar.get(), 0, 255)
            saturationHsv2 = (self.__hueMaxVar.get(), 255, 255)
            saturationRgb1 = self.__hsvToRgb(saturationHsv1)
            saturationRgb2 = self.__hsvToRgb(saturationHsv2)
            saturationColor1 = "#%02x%02x%02x" % saturationRgb1
            saturationColor2 = "#%02x%02x%02x" % saturationRgb2
            if self.__saturationMaxSeek != None:
                self.__saturationMaxSeek.configure(seekBg1 = saturationColor1, seekBg2 = saturationColor2)

    def __updateMaxValueColor(self):
            valueHsv1 = (self.__hueMaxVar.get(), self.__saturationMaxVar.get(), 0)
            valueHsv2 = (self.__hueMaxVar.get(), self.__saturationMaxVar.get(), 255)
            valueRgb1 = self.__hsvToRgb(valueHsv1)
            valueRgb2 = self.__hsvToRgb(valueHsv2)
            valueColor1 = "#%02x%02x%02x" % valueRgb1
            valueColor2 = "#%02x%02x%02x" % valueRgb2
            if(self.__valueMaxSeek != None):
                self.__valueMaxSeek.configure(seekBg1 = valueColor1, seekBg2 = valueColor2)

    def __onHueMinChanged(self, *args):
        try:
            self.__updateMinSaturationColor()
            self.__updateMinValueColor()
            self.__hueValueLabel.configure(text = str(self.__hueMinVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __onSaturationMinChanged(self, *args):
        try:
            self.__updateMinValueColor()
            self.__saturationValueLabel.configure(text = str(self.__saturationMinVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __onValueMinChanged(self, *args):
        try:
            self.__valueValueLabel.configure(text=str(self.__valueMinVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __onHueMaxChanged(self, *args):
        try:
            self.__updateMaxSaturationColor()
            self.__updateMaxValueColor()
            self.__hueValueLabel2.configure(text = str(self.__hueMaxVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __onSaturationMaxChanged(self, *args):
        try:
            self.__updateMaxValueColor()
            self.__saturationValueLabel2.configure(text = str(self.__saturationMaxVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __onValueMaxChanged(self, *args):
        try:
            self.__valueValueLabel2.configure(text=str(self.__valueMaxVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __onContourMinChanged(self, *args):
        try:
            self.__contourMinValueLabel.configure(text=str(self.__contourMinVar.get()))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
            return

    def __initContourDetectorSettingsWidgets(self):

        bg = PIL.Image.open("Assets/hue.jpg")

        # Lower border
        self.__lowerMaskLabel = tk.Label(master = self, text="Lower mask border")
        self.__lowerMaskLabel.pack(fill=tk.X, side=tk.TOP)

        # Hue min
        self.__hueMinFrame = tk.Frame(master = self)
        self.__hueLabel = tk.Label(master = self.__hueMinFrame, text = 'Hue: ')
        self.__hueLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__hueValueLabel = tk.Label(master = self.__hueMinFrame, text = '0')
        self.__hueValueLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__hueMinFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__hueMinSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5, seekBgImage = bg,
                                       maxVal=255, minVal=0)
        self.__hueMinSeek.setVariable(self.__hueMinVar)
        self.__hueMinSeek.setValue(0)
        self.__hueMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(0,5), padx=20)

        # Saturtation min
        self.__saturationMinFrame = tk.Frame(master = self)
        self.__saturationLabel = tk.Label(master = self.__saturationMinFrame, text = 'Saturtation: ')
        self.__saturationLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__saturationValueLabel = tk.Label(master = self.__saturationMinFrame, text = '0')
        self.__saturationValueLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__saturationMinFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__saturationMinSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5,
                                              seekBg2 = '#FF0000', seekBg1 = '#FFFFFF', maxVal=255, minVal=0)
        self.__saturationMinSeek.setVariable(self.__saturationMinVar)
        self.__saturationMinSeek.setValue(0)
        self.__saturationMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(0,5), padx=20)

        # Value min
        self.__valueMinFrame = tk.Frame(master = self)
        self.__valueLabel = tk.Label(master = self.__valueMinFrame, text = 'Value: ')
        self.__valueLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__valueValueLabel = tk.Label(master = self.__valueMinFrame, text = '0')
        self.__valueValueLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__valueMinFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__valueMinSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5,
                                              seekBg1 = '#000000', seekBg2 = '#FFFFFF', maxVal=255, minVal=0)
        self.__valueMinSeek.setVariable(self.__valueMinVar)
        self.__valueMinSeek.setValue(0)
        self.__valueMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(0,5), padx=20)

        # Delimiter
        self.__maskSettingsDelimiter = tk.Frame(master = self, height=20)
        self.__maskSettingsDelimiter.pack(fill=tk.X, side=tk.TOP)

        # Upper border
        self.__upperMaskLabel = tk.Label(master = self, text="Upper mask border")
        self.__upperMaskLabel.pack(fill=tk.X, side=tk.TOP)

        # Hue max
        self.__hueMaxFrame = tk.Frame(master = self)
        self.__hueLabel2 = tk.Label(master = self.__hueMaxFrame, text = 'Hue: ')
        self.__hueLabel2.pack(fill=tk.X, side=tk.LEFT)
        self.__hueValueLabel2 = tk.Label(master = self.__hueMaxFrame, text = '0')
        self.__hueValueLabel2.pack(fill=tk.X, side=tk.LEFT)
        self.__hueMaxFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__hueMaxSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5, seekBgImage = bg,
                                       maxVal=255, minVal=0)
        self.__hueMaxSeek.setVariable(self.__hueMaxVar)
        self.__hueMaxSeek.setValue(255)
        self.__hueMaxSeek.pack(fill=tk.X, side=tk.TOP, pady=(0,5), padx=20)

        # Saturation max
        self.__saturationMaxFrame = tk.Frame(master = self)
        self.__saturationLabel2 = tk.Label(master = self.__saturationMaxFrame, text = 'Saturation: ')
        self.__saturationLabel2.pack(fill=tk.X, side=tk.LEFT)
        self.__saturationValueLabel2 = tk.Label(master = self.__saturationMaxFrame, text = '0')
        self.__saturationValueLabel2.pack(fill=tk.X, side=tk.LEFT)
        self.__saturationMaxFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__saturationMaxSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5,
                                              seekBg2 = '#FF0000', seekBg1 = '#FFFFFF',
                                              maxVal=255, minVal=0)
        self.__saturationMaxSeek.setVariable(self.__saturationMaxVar)
        self.__saturationMaxSeek.setValue(255)
        self.__saturationMaxSeek.pack(fill=tk.X, side=tk.TOP, pady=(0, 5), padx=20)

        # Value max
        self.__valueMaxFrame = tk.Frame(master = self)
        self.__valueLabel2 = tk.Label(master = self.__valueMaxFrame, text = 'Value: ')
        self.__valueLabel2.pack(fill=tk.X, side=tk.LEFT)
        self.__valueValueLabel2 = tk.Label(master = self.__valueMaxFrame, text = '0')
        self.__valueValueLabel2.pack(fill=tk.X, side=tk.LEFT)
        self.__valueMaxFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__valueMaxSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5,
                                              seekBg2 = '#FF0000', seekBg1 = '#000000',
                                              maxVal=255, minVal=0)
        self.__valueMaxSeek.setVariable(self.__valueMaxVar)
        self.__valueMaxSeek.setValue(255)
        self.__valueMaxSeek.pack(fill=tk.X, side=tk.TOP, pady=(0,5), padx=20)

        # Delimiter
        self.__maskSettingsDelimiter2 = tk.Frame(master = self, height=20)
        self.__maskSettingsDelimiter2.pack(fill=tk.X, side=tk.TOP)

        # Contour area
        self.__minContourAreaLabel = tk.Label(master = self, text="Contour area")
        self.__minContourAreaLabel.pack(fill=tk.X, side=tk.TOP)

        self.__contourMinFrame = tk.Frame(master = self)
        self.__contourMinLabel = tk.Label(master = self.__contourMinFrame, text = 'Min contour area: ')
        self.__contourMinLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__contourMinValueLabel = tk.Label(master = self.__contourMinFrame, text = '0')
        self.__contourMinValueLabel.pack(fill=tk.X, side=tk.LEFT)
        self.__contourMinFrame.pack(fill=tk.X, side=tk.TOP, pady=(5,0), padx=20)

        self.__contourAreaMinSeek = mw.SeekBar(master = self, pinColor = 'black', pinWidth = 5,
                                              seekBg = '#CCCCCC',
                                              maxVal=1000, minVal=0)
        self.__contourAreaMinSeek.setVariable(self.__contourMinVar)
        self.__contourAreaMinSeek.setValue(0)
        self.__contourAreaMinSeek.pack(fill=tk.X, side=tk.TOP, pady=(0,5), padx=20)
