
import random

class Map:

    map_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '#']

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height

        num_map_values = len(self.map_values)

        # Create a matrix of size [width][height]
        self.map = [[self.map_values[random.randint(0, num_map_values - 1)] for i in range(self.width)] for i in range(self.height)]

        # Add a starting and goal positions
        self.map[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)] = 'S'
        self.map[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)] = 'G'

    def get_map(self):
        return self.map

m = Map()
print(m.get_map())