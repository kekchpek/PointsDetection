import tkinter as tk
import traceback

import MyWidgets as mw

class HSVRangeDisplay(tk.Frame):

    def __init__(self, master, hueMinVar, saturationMinVar, valueMinVar, hueMaxVar,
                saturationMaxVar, valueMaxVar, **kw):
        width = 400
        height = 400
        if 'width' in kw:
            width = kw['width']
        else:
            kw['width'] = width
        if 'height' in kw:
            height = kw['height']
        else:
            kw['height'] = height
        super().__init__(master=master, cnf={}, **kw)
        self.__hueMinVar = hueMinVar
        self.__saturationMinVar = saturationMinVar
        self.__valueMinVar = valueMinVar
        self.__hueMaxVar = hueMaxVar
        self.__saturationMaxVar = saturationMaxVar
        self.__valueMaxVar = valueMaxVar

        self.__createWidgets(width, height)

        self.__hueMinVar.trace_add('write', self.__onHueMinChanged)
        self.__saturationMinVar.trace_add('write', self.__onSaturationMinChanged)
        self.__valueMinVar.trace_add('write', self.__onValueMinChanged)
        self.__hueMaxVar.trace_add('write', self.__onHueMaxChanged)
        self.__saturationMaxVar.trace_add('write', self.__onSaturationMaxChanged)
        self.__valueMaxVar.trace_add('write', self.__onValueMaxChanged)

    def __onHueMinChanged(self, *args):
        try:
            self.__minHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__maxHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__minHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
            self.__maxHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __onSaturationMinChanged(self, *args):
        try:
            self.__minHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__maxHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__minHV.setHSVSaturation(self.__saturationMinVar.get())
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __onValueMinChanged(self, *args):
        try:
            self.__minHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
            self.__maxHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
            self.__minHS.setHSVValue(self.__valueMinVar.get())
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __onHueMaxChanged(self, *args):
        try:
            self.__minHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__maxHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__minHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
            self.__maxHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __onSaturationMaxChanged(self, *args):
        try:
            self.__minHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__maxHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__saturationMinVar.get(), self.__saturationMaxVar.get())
            self.__maxHV.setHSVSaturation(self.__saturationMaxVar.get())
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __onValueMaxChanged(self, *args):
        try:
            self.__minHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
            self.__maxHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                      self.__valueMinVar.get(), self.__valueMaxVar.get())
            self.__maxHS.setHSVValue(self.__valueMaxVar.get())
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            traceback.print_exc()

    def __createWidgets(self, width, height):
        if width <= 8 or height <= 8:
            return
        tileWidth = int((width - 8) / 2)
        tileHeight = int((height - 8) / 2)

        # min HS
        self.__minHS = mw.CanvasHS(master=self, width=tileWidth, height = tileHeight)
        self.__minHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                  self.__saturationMinVar.get(), self.__saturationMaxVar.get())
        self.__minHS.setHSVValue(self.__valueMinVar.get())
        self.__minHS.pack_propagate(0)
        self.__minHS.place(rely=0.25, relx=0.25, anchor='c')

        # max HS
        self.__maxHS = mw.CanvasHS(master = self, width=tileWidth, height = tileHeight)
        self.__maxHS.setHSBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                  self.__saturationMinVar.get(), self.__saturationMaxVar.get())
        self.__maxHS.setHSVValue(self.__valueMaxVar.get())
        self.__maxHS.pack_propagate(0)
        self.__maxHS.place(rely=0.75, relx=0.25, anchor='c')

        # min HV
        self.__minHV = mw.CanvasHV(master=self, width=tileWidth, height = tileHeight)
        self.__minHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                  self.__valueMinVar.get(), self.__valueMaxVar.get())
        self.__minHV.setHSVSaturation(self.__saturationMinVar.get())
        self.__minHV.pack_propagate(0)
        self.__minHV.place(rely=0.25, relx=0.75, anchor='c')

        # max HV
        self.__maxHV = mw.CanvasHV(master=self, width=tileWidth, height = tileHeight)
        self.__maxHV.setHVBorders(self.__hueMinVar.get(), self.__hueMaxVar.get(),
                                  self.__valueMinVar.get(), self.__valueMaxVar.get())
        self.__maxHV.setHSVSaturation(self.__saturationMaxVar.get())
        self.__maxHV.pack_propagate(0)
        self.__maxHV.place(rely=0.75, relx=0.75, anchor='c')


