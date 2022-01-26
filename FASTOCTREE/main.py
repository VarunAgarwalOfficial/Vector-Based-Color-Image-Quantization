from PIL import Image 
import os
import json


img_path = input("Enter the path of the image: ")


try:
    os.mkdir(f"results/{img_path.split('.')[0]}")
except:
    pass
for no in range(2,9):
    image = Image.open("images/"+img_path)
    path = f"results/{img_path.split('.')[0]}/k{2**no}/"
    try:
        os.mkdir(path)
    except:
        pass

    im = image.quantize(2**no , method=2)

    
    im = im.convert('RGB')
    im.save(path+"reconstructed.png")
    errors = {"MSE" : 0, "MAE" : 0}

    width, height = image.size
    for i in range(width):
        for j in range(height):
            r, g, b  = image.getpixel((i, j))
            r1, g1, b1  = im.getpixel((i, j))
            errors["MSE"] += (r-r1)**2 + (g-g1)**2 + (b-b1)**2
            errors["MAE"] += abs(r-r1) + abs(g-g1) + abs(b-b1)

    errors["MSE"] = errors["MSE"] / (width*height)
    errors["MAE"] = errors["MAE"] / (width*height)

    '''
    Save the result matrics
    '''
    with open(f"{path}result.json", "w") as f:
        json.dump(errors, f)
