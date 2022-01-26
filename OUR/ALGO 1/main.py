from re import I
from PIL import Image




def distance(a, b):
    return sum([abs(a[i] - b[i]) for i in range(3)])


def merge(colors):
    new_colors = []
    new_colors_count = []
    MAX_DISTANCE = 50
    for index , color in enumerate(colors.keys()):
        min_dist = float('inf')
        min_color = None
        for i,new_color in enumerate(new_colors):
            dist = distance(color, new_color)
            if dist < min_dist:
                min_dist = dist
                min_color = i
        if min_dist > MAX_DISTANCE:
            new_colors.append(color)
            new_colors_count.append(colors[color])
        else:
            new_colors[min_color] = ((new_colors[min_color][0]*new_colors_count[min_color] + color[0]*colors[color]),(new_colors[min_color][1]*new_colors_count[min_color] + color[1]*colors[color]) , (new_colors[min_color][2]*new_colors_count[min_color] + color[2]*colors[color]))
            new_colors_count[min_color] += colors[color]

            new_colors[min_color] = (new_colors[min_color][0]/new_colors_count[min_color],new_colors[min_color][1]/new_colors_count[min_color],new_colors[min_color][2]/new_colors_count[min_color])
    new_colors_count, new_colors = zip(*sorted(zip(new_colors_count, new_colors)))
    return list(new_colors)



def reconstruct(pallete, img , img_path):
    width, height = img.size
    im2 = Image.new(mode="RGB", size=(width, height))
    pixels = im2.load()
    for i in range(width):
        for j in range(height):
            r, g, b  = img.getpixel((i, j))

            min_dist = float('inf')
            min_index = 0
            for k in range(len(pallete)):
                if distance(pallete[k], (r, g, b)) < min_dist:
                    min_dist = distance(pallete[k], (r, g, b))
                    min_index = k
            
            # print(f"{i} {j} {min_index}")
            pixels[i,j] =  pallete[min_index]
    

    im2.show()
    im2.save("images/re/" + img_path)


def main():
    # K =
    img_path = 'Lenna.png'
    # Open the image
    img = Image.open(f"images/{img_path}")
    pixels = img.load()
    width, height = img.size


    colors = {}
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i,j]
            colors[(r,g,b)] = colors.get((r,g,b), 0) + 1
    

    pallete = merge(colors)
    print(len(pallete))
    # pallete = pallete[0:K]
    for i in range(len(pallete)):
        pallete[i] = (int(pallete[i][0]) , int(pallete[i][1]) , int(pallete[i][2]))
    im = Image.new(mode="RGB", size=(100*len(pallete), 200))
    for i, color in enumerate(pallete):
        im.paste(color, (i*100, 0, (i+1)*100, 200))
    im.show()

    reconstruct(pallete, img, img_path)

if __name__ == "__main__":
    main()