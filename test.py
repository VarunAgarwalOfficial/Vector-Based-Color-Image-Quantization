images = ["lenna" , "airplane" , "mandril" , "pepper" , "sailboat"]
from PIL import Image
import os



files = os.listdir('./images')

for img in files:
    im = Image.open('./images/'+img)
    colors = {}

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if im.getpixel((i,j)) not in colors:
                colors[im.getpixel((i,j))] = 1
    print(img + ": " + str(len(colors)))


