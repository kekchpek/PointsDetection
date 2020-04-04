import colorsys
import cv2 as cv
import PIL
from Application import Application
import tkinter as tk
import numpy as np

byteArray = np.full((256,256,3), 255)
for i in range(256):
    for j in range(256):
        byteArray[j, i] = (i, 255, 255)
img = cv.cvtColor(byteArray.astype('uint8'), cv.COLOR_HSV2RGB)
img = PIL.Image.fromarray(img.astype(np.uint8))
img.save('dsf.jpg')

root = tk.Tk()
app = Application(master=root)
app.mainloop()
app.dispose()