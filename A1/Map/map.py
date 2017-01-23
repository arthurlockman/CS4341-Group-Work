
import random

class Map:

    map_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '#']

    def __init__(self, width, height, _map):
        self.map = _map
        self.width = width
        self.height = height
 

    def get_map(self):
        return self.map

    def write_to_file(self, filename):
        with open(filename, 'w+') as f:
            for row in range(len(self.map)):
                for col in range(len(self.map[0])):
                    # Write the map character
                    f.write(self.map[row][col])

                    # Write a tab after each character, so long as it's not the last in the line
                    if(col != len(self.map[0])-1):
                        f.write('\t')

                # Newline for every row
                f.write('\n')


    @classmethod
    def read_from_file(cls, filename):
        with open(filename, 'r') as f:
            file_contents = f.readlines()
            _map = [x.strip().split('\t') for x in file_contents]
            height = len(_map)
            width = len(_map[0])
            return cls(width, height, _map)

    @classmethod
    def create_new_map(cls, width=10, height=10):
        num_map_values = len(cls.map_values)

        # Create a matrix of size [width][height]
        _map = [[cls.map_values[random.randint(0, num_map_values - 1)] for i in range(width)] for i in range(height)]

        # Add a starting and goal positions
        _map[random.randint(0, width - 1)][random.randint(0, height - 1)] = 'S'
        _map[random.randint(0, width - 1)][random.randint(0, height - 1)] = 'G'

        return cls(width, height, _map)

# Map.read_from_file('map.txt').write_to_file('tmp.txt')
# print(Map.read_from_file('tmp.txt').get_map())

