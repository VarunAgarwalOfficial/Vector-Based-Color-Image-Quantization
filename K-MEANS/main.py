import cv2
import numpy as np
from PIL import Image
import os
import json
def quantimage(image,k):
    i = np.float32(image).reshape(-1,3)
    condition = (cv2.TERM_CRITERIA_MAX_ITER,1,1.0)
    ret,label,center = cv2.kmeans(i, k , None, condition,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    final_img = center[label.flatten()]
    final_img = final_img.reshape(image.shape)
    return final_img



img = input("Emter the image name: ")
image = cv2.imread("images/" + img)
im = Image.open("images/" + img)

try:
    os.mkdir(f"results/{img.split('.')[0]}")
except:
    pass


for no in range(2,9):
    path = f"results/{img.split('.')[0]}/k{2**no}"
    try:
        os.mkdir(path)
    except:
        pass
    cv2.imwrite(f'results/{img.split(".")[0]}/k{2**no}/reconstructed.png' , quantimage(image,2**no))
    errors = {"MSE" : 0, "MAE" : 0}
    re = Image.open(f'results/{img.split(".")[0]}/k{2**no}/reconstructed.png')

    width, height = im.size
    for i in range(width):
        for j in range(height):
            r, g, b  = im.getpixel((i, j))
            r1, g1, b1  = re.getpixel((i, j))
            errors["MSE"] += (r-r1)**2 + (g-g1)**2 + (b-b1)**2
            errors["MAE"] += abs(r-r1) + abs(g-g1) + abs(b-b1)

    errors["MSE"] = errors["MSE"] / (width*height)
    errors["MAE"] = errors["MAE"] / (width*height)

    '''
    Save the result matrics
    '''
    with open(f'results/{img.split(".")[0]}/k{2**no}/result.json', "w") as f:
        json.dump(errors, f)
