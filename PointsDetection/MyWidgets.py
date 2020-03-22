from tkinter import Canvas
from PIL import Image
from PIL import ImageTk


class ImageCanvas(Canvas):

    def settleImageData(self, imgData):
        rawImg = Image.fromarray(imgData)
        imgWidth = rawImg.width
        imgHeight = rawImg.height
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        scale = min(width/imgWidth, height/imgHeight)
        rawImg = rawImg.resize(tuple([int(scale*x) for x in rawImg.size]), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(rawImg)
        self.create_image(width/2, height/2, anchor='c', image = img)
        self.__image = img