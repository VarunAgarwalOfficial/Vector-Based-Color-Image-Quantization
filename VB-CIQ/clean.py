from PIL import Image
from Node import Node
import os
import math
import json

'''
Returns the distance between two colors
'''
def distance(a, b):
    return sum([abs(a[i] - b[i]) for i in range(3)])

'''
Returns a list of colors and their counts
'''
def get_colors(img):
    '''
    Load the image and loop through all the pixels
    '''
    pixel_map = img.load()
    width, height = img.size
    colors = {}
    for x in range(width):
        for y in range(height):
            r, g, b = pixel_map[x, y]
            '''
            if the color is already in the dictionary then increment the count else add the color to the dictionary
            '''
            colors[(r, g, b)] = colors.get((r, g, b), 0) + 1
    
    '''
    return the colors dictionary
    '''
    return colors





'''
Initial Reduction to save computation time
'''
def reduce(colors , max_distance):

    new_colors = []
    new_colors_count = []
    
    '''
    loop over all the colors 
    '''
    for color in list(colors.keys()):
        min_dist = float('inf')
        min_color = None

        '''
        loop over all the new colors
        '''
        for i,new_color in enumerate(new_colors):
            '''
            find the distance between the current color and the new color
            '''
            dist = distance(color, new_color)
            '''
            if the distance is less than the min distance then update the min distance and min color
            '''
            if dist < min_dist:
                min_dist = dist
                min_color = i

        '''
        if no suitable colors in the new color list , add the current color to the new color list
        '''
        if min_dist > max_distance:
            new_colors.append(color)
            new_colors_count.append(colors[color])
        else:
            '''
            take the weighted mean of the new color to the closest color
            '''
            new_colors[min_color] = ((new_colors[min_color][0]*new_colors_count[min_color] + color[0]*colors[color]),(new_colors[min_color][1]*new_colors_count[min_color] + color[1]*colors[color]) , (new_colors[min_color][2]*new_colors_count[min_color] + color[2]*colors[color]))
            new_colors_count[min_color] += colors[color]
            new_colors[min_color] = (new_colors[min_color][0]/new_colors_count[min_color],new_colors[min_color][1]/new_colors_count[min_color],new_colors[min_color][2]/new_colors_count[min_color])
    


    '''
    round all the new colors to the nearest integer
    '''
    for i in range(len(new_colors)):
        new_colors[i] = (int(new_colors[i][0]) , int(new_colors[i][1]) , int(new_colors[i][2]))


    '''
    Convert the new colors to a dictionary
    '''
    colors = {}
    for i in range(len(new_colors)):
        colors[new_colors[i]] = new_colors_count[i]
    
    '''
    Return the new colors
    '''
    return colors
        


'''
Makes an undirected weighted graph from the colors
'''
def make_graph(colors , max_distance):
    graph = []
    '''
    Gey the keys of the colors dictionary
    '''
    keys = list(colors.keys())

    '''
    Loop over all the colors and add a node for that color to the graph
    '''

    for i in keys:
        graph.append(Node(colors[i] , i))


    '''
    Loop over all the colors and add an edge between the the colors which are neighbors
    '''
    for i in range(len(keys)):
        if i % 100 == 0:
            print(f"At Key : {i}")


        for j in range(i+1, len(keys)):
            if distance(keys[i], keys[j]) < max_distance:
                '''
                if the distance is less than the max distance then add an edge between the two colors
                '''
                graph[i].add_neighbor(graph[j])
                graph[j].add_neighbor(graph[i])
    
    '''
    return the graph
    '''
    return graph



'''
Select the best color from the graph
'''
def select_best_color(graph):
    '''
    Initialize the best color to the first color in the graph
    '''

    best_node_weight = 0
    best_node_index = 0

    for i in range(len(graph)):
        '''
        calculate the weight of the each node 
        '''
        weight = graph[i].value
        for neighbor in graph[i].neighbors:
            weight += neighbor.value
        

        '''
        if the weight of the node is greater than the best weight then update the best weight and best node index
        '''
        if weight > best_node_weight:
            best_node_weight = weight
            best_node_index = i


    best_node = graph[best_node_index]
    neighbors = graph[best_node_index].neighbors


    '''
    Remove the best node and its neighbors from the graph
    '''
    
    for i in graph:
        '''
        remove the node as neighbor from all the nodes
        '''
        i.remove_neighbor(best_node)
        for neighbor in neighbors:
            i.remove_neighbor(neighbor)
    
    '''
    remove neighbors from the graph
    '''


    for neighbor in neighbors:
        graph.remove(neighbor)

    
    color = best_node.color
    
    '''
    remove the best node from the graph
    '''

    graph.remove(best_node)
    return color,graph



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
    img_name = input("Image Name: ")
    img = Image.open("images/" + img_name)
    
    colors = get_colors(img)
    print(f"Original Image has {len(colors)} colors")
    

    K = [8,16,32,64,128,256]
    reduction_distance = [40,35,28,25,15,10]
    graph_connections = [38,50,55,40,20,15]



    '''
    Make the Result Directory
    '''
    try:
        os.mkdir(f"results/{img_name.split('.')[0]}")
    except:
        pass

    for i in range(len(K)):
        print(f"Reducing Colors to {K[i]}")
        reduced_colors = reduce(colors,reduction_distance[i])
        print(f"New Colors : {len(reduced_colors)}")
        graph = make_graph(reduced_colors , graph_connections[i])
        print(f"Finished makeing the graph")
        palette = []

        '''
        Select the BEST color from the graph k times
        '''
        for k in range(K[i]):
            color,graph = select_best_color(graph)
            palette.append(color)


        '''
        Make the directory results/{img_name}/k{K[i]}} 
        '''
        path = f"results/{img_name.split('.')[0]}/k{K[i]}"
        try:
            os.mkdir(path)
        except:
            pass
        print(f"Saving Palette with {K[i]} colors")

        '''
        Save the palette as text
        '''
        with open(f"{path}/palette.txt", "w") as f:
            for color in palette:
                f.write(f"({color[0]} , {color[1]} , {color[2]}),\n")
        

        '''
        Save the palette as image 
        '''
        im = Image.new(mode="RGB", size=(100*len(palette), 200))
        for pos, color in enumerate(palette):
            im.paste(color, (pos*100, 0, (pos+1)*100, 200))
        im.save(f"{path}/palette.png")


        '''
        Save the reconstructed image
        '''
        reconstruct(img,palette,f"{path}/reconstructed.png")
        

        '''
        calculating result matrics
        '''
        errors = {"MSE" : 0, "MAE" : 0}
        orig = Image.open("images/" + img_name)

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