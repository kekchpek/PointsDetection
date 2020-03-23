from tkinter import Canvas
from PIL import Image
from PIL import ImageTk


class ImageCanvas(Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        super(ImageCanvas, self).__init__(master, cnf, **kw)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def settleImageData(self, imgData):
        rawImg = Image.fromarray(imgData)
        imgWidth = rawImg.width
        imgHeight = rawImg.height
        scale = min(self.width/imgWidth, self.height/imgHeight)
        rawImg = rawImg.resize(tuple([int(scale*x) for x in rawImg.size]), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(rawImg)
        self.create_image(self.width/2, self.height/2, anchor='c', image = img)
        self.__image = img