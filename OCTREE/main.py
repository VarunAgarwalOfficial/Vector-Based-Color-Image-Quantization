from PIL import Image
import os
import json
import math

def dist(col1,col2):
    return ((col1[0]-col2[0])**2 + (col1[1]-col2[1])**2 + (col1[2]-col2[2])**2)**0.5


def add(pallete , color , K):
    pallete.append(color)

    if len(pallete) > K:
        min_dist = float('inf')
        min_index = (-1, -1)
        for i in range(len(pallete)):
            for j in range(i+1,len(pallete)):
                if dist(pallete[i], pallete[j]) < min_dist:
                    min_dist = dist(pallete[i], pallete[j])
                    min_index = (i, j)
        

        a = pallete[min_index[0]]
        b = pallete[min_index[1]]

        new_p = []

        for i in range(len(pallete)):
            if i not in min_index:
                new_p.append(pallete[i])

        new_p.append(((a[0]+b[0])//2, (a[1]+b[1])//2, (a[2]+b[2])//2))

        return new_p
    return pallete


def reconstruct(img,palette,output_path):
    def eu_distance(a,b):
        return math.sqrt(sum([(a[i]-b[i])**2 for i in range(len(a))]))
    '''
    Load the image and loop through all the pixels
    '''
    pixel_map = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):

            r, g, b = pixel_map[x, y]

            '''
            find the nearest color in the palette for the pixel
            '''

            min_dist = float('inf')
            min_color = None

            for i in range(len(palette)):
                dist = eu_distance((r, g, b), palette[i])
                if dist < min_dist:
                    min_dist = dist
                    min_color = i


            '''
            set the pixel to the nearest color
            '''
            pixel_map[x, y] = palette[min_color]
    

    '''
    save the image
    '''
    img.save(output_path)

def main():
    img_path = input("Enter Image Name :")
    # Open the image
    img = Image.open(f"images/{img_path}")
    width, height = img.size

    try:
        os.mkdir(f"results/{img_path.split('.')[0]}")
    except:
        pass

    for no in range(2,9):
        K = 2**no
        path = f"results/{img_path.split('.')[0]}/k{2**no}"
        try:
            os.mkdir(path)
        except:
            pass
        palette = []
        for i in range(width):
            for j in range(height):
                r, g, b  = img.getpixel((i, j))
                palette = add(palette, (r, g, b) , K = 2**no)
 
        print(f"Saving K : {K}")
        im = Image.new(mode="RGB", size=(100*len(palette), 200))
        for i, color in enumerate(palette):
            im.paste(color, (i*100, 0, (i+1)*100, 200))
        im.save(f'results/{img_path.split(".")[0]}/k{2**no}/palette.png')

        reconstruct(img,palette,f"{path}/reconstructed.png")

        errors = {"MSE" : 0, "MAE" : 0}
        orig = Image.open("images/" + img_path)

        width, height = img.size
        for i in range(width):
            for j in range(height):
                r, g, b  = img.getpixel((i, j))
                r1, g1, b1  = orig.getpixel((i, j))
                errors["MSE"] += (r-r1)**2 + (g-g1)**2 + (b-b1)**2
                errors["MAE"] += abs(r-r1) + abs(g-g1) + abs(b-b1)

        errors["MSE"] = errors["MSE"] / (width*height)
        errors["MAE"] = errors["MAE"] / (width*height)

        '''
        Save the result matrics
        '''
        with open(f"{path}/result.json", "w") as f:
            json.dump(errors, f)

        

        img = orig



    



if __name__ == '__main__':
    main()
