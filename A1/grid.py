import random
import math
from gridcell import GridCell


class Grid:
    grid_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, math.inf]

    def __init__(self, width, height, grid, start_pos, goal_pos):
        self.grid = grid
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.goal_pos = goal_pos

    def get_cell(self, row, col):
        return self.grid[row][col]

    def get_grid(self):
        return self.grid

    def get_start_position(self):
        return self.start_pos

    def get_goal_position(self):
        return self.goal_pos

    def get_start_cell(self):
        return self.grid[self.start_pos[0]][self.start_pos[1]]

    def get_goal_cell(self):
        return self.grid[self.goal_pos[0]][self.goal_pos[1]]

    def write_to_file(self, filename):
        with open(filename, 'w+') as f:
            f.write(str(self))

    def __str__(self):
        _str = ''
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):

                if (row, col) == self.start_pos:
                    _str += 'S'
                elif (row, col) == self.goal_pos:
                    _str += 'G'
                else:
                    _str += self.grid[row][col].write_to_string()

                # Write a tab after each character, so long as it's not the last in the line
                if (col != len(self.grid[0]) - 1):
                    _str += '\t'

            # Newline for every row
            _str += '\n'
        return _str

    def __repr__(self):
        return self.__str__()

    @classmethod
    def read_from_file(cls, filename):
        with open(filename, 'r') as f:
            file_contents = f.readlines()

            # Load in the grid, replacing hashtags with infinity and casting all numbers to ints
            symbolic_grid = [
                [math.inf if item == '#' else (item if (item == 'S' or item == 'G') else int(item)) for item in
                 x.strip().split('\t')] for x in file_contents]
            height = len(symbolic_grid)
            width = len(symbolic_grid[0])

            for row in range(height):
                for col in range(width):
                    if symbolic_grid[row][col] == 'S':
                        start_pos = (row, col)
                        symbolic_grid[row][col] = 1
                    if symbolic_grid[row][col] == 'G':
                        goal_pos = (row, col)
                        symbolic_grid[row][col] = 1

            grid = [[GridCell((row, col), goal_pos, symbolic_grid[row][col]) for col in range(width)] for row in
                    range(height)]

            return cls(width, height, grid, start_pos, goal_pos)

    @classmethod
    def create_new_grid(cls, width=10, height=10):
        num_map_values = len(cls.grid_values)

        # Create start and goal positions
        start = (random.randint(0, width - 1), random.randint(0, height - 1))
        goal = (random.randint(0, width - 1), random.randint(0, height - 1))

        # Create a matrix of size [height][width]
        grid = [
            [GridCell((row, col), goal, cls.grid_values[random.randint(0, num_map_values - 1)]) for col in range(width)]
            for row in range(height)]

        # Add a starting and goal positions
        grid[start[0]][start[1]].set_cell_cost(1)
        grid[goal[0]][goal[1]].set_cell_cost(1)

        return cls(width, height, grid, start, goal)


# UNIT TESTS
g = Grid.read_from_file('grid10.txt')
# assert(g.get_start_cell().pos)
