class Node:
    def __init__(self, value , color):
        self.value = value
        self.color = color
        self.neighbors = []
    
    def add_neighbor(self,neighbor):
        self.neighbors.append(neighbor)
    

    def remove_neighbor(self,neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)