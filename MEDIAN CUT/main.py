import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.io import imsave
import os
from PIL import Image
import json


def median_cut_quantize(img, img_arr):
    r_average = np.mean(img_arr[:,0])
    g_average = np.mean(img_arr[:,1])
    b_average = np.mean(img_arr[:,2])
    
    for data in img_arr:
        sample_img[data[3]][data[4]] = [r_average, g_average, b_average]
    
def split_into_buckets(img, img_arr, depth):
    
    if len(img_arr) == 0:
        return 
        
    if depth == 0:
        median_cut_quantize(img, img_arr)
        return
    
    r_range = np.max(img_arr[:,0]) - np.min(img_arr[:,0])
    g_range = np.max(img_arr[:,1]) - np.min(img_arr[:,1])
    b_range = np.max(img_arr[:,2]) - np.min(img_arr[:,2])
    
    space_with_highest_range = 0

    if g_range >= r_range and g_range >= b_range:
        space_with_highest_range = 1
    elif b_range >= r_range and b_range >= g_range:
        space_with_highest_range = 2
    elif r_range >= b_range and r_range >= g_range:
        space_with_highest_range = 0


    # sort the image pixels by color space with highest range 
    # and find the median and divide the array.
    img_arr = img_arr[img_arr[:,space_with_highest_range].argsort()]
    median_index = int((len(img_arr)+1)/2)

    
    #split the array into two blocks
    split_into_buckets(img, img_arr[0:median_index], depth-1)
    split_into_buckets(img, img_arr[median_index:], depth-1)
    



img = input("Enter the image name : ")
sample_img = imread('images/'+img)
try:
    os.mkdir(f"results/{img.split('.')[0]}")
except:
    pass


for i in range(2,9):
    flattened_img_array = []
    for rindex, rows in enumerate(sample_img):
        for cindex, color in enumerate(rows):
            flattened_img_array.append([color[0],color[1],color[2],rindex, cindex]) 

    flattened_img_array = np.array(flattened_img_array)
    split_into_buckets(sample_img, flattened_img_array, i)


    path = f"results/{img.split('.')[0]}/k{2**i}"
    try:
        os.mkdir(path)
    except:
        pass

    imsave(f'results/{img.split(".")[0]}/k{2**i}/reconstructed.png', sample_img)
    sample_img = imread('images/'+img)




im = Image.open("images/" + img)
for no in range(2,9):
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
