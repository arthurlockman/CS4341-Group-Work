
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
 

    def get_grid(self):
        return self.grid

    def write_to_file(self, filename):
        with open(filename, 'w+') as f:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):

                    if (row, col) == self.start_pos:
                        f.write('S')
                    elif (row, col) == self.goal_pos:
                        f.write('G')
                    else:
                        f.write(self.grid[row][col].__str__())

                    # Write a tab after each character, so long as it's not the last in the line
                    if(col != len(self.grid[0])-1):
                        f.write('\t')

                # Newline for every row
                f.write('\n')


    @classmethod
    def read_from_file(cls, filename, heuristic=1):
        with open(filename, 'r') as f:
            file_contents = f.readlines()

            # Load in the grid, replacing hashtags with infinity and casting all numbers to ints
            symbolic_grid = [[math.inf if item == '#' else (item if (item == 'S' or item == 'G') else int(item)) for item in x.strip().split('\t')] for x in file_contents]
            height = len(symbolic_grid)
            width = len(symbolic_grid[0])

            for row in range(height):
                for col in range(width):
                    if symbolic_grid[row][col] == 'S':
                        start_pos = (row, col)
                    if symbolic_grid[row][col] == 'G':
                        goal_pos = (row, col)

            grid = [[ GridCell((row, col), goal_pos, symbolic_grid[row][col], heuristic) for col in range(width)] for row in range(height)]

            return cls(width, height, grid, start_pos, goal_pos)

    @classmethod
    def create_new_grid(cls, width=10, height=10, heuristic=1):
        num_map_values = len(cls.grid_values)

        # Create start and goal positions
        start = (random.randint(0, width - 1), random.randint(0, height - 1))
        goal = (random.randint(0, width - 1), random.randint(0, height - 1))

        # Create a matrix of size [height][width]
        grid = [[ GridCell((row, col), goal, cls.grid_values[random.randint(0, num_map_values - 1)], heuristic) for col in range(width)] for row in range(height)]

        # Add a starting and goal positions
        grid[start[0]][start[1]].set_cell_cost(1)
        grid[goal[0]][goal[1]].set_cell_cost(1)

        return cls(width, height, grid, start, goal)


# UNIT TESTS
# Grid.create_new_grid().write_to_file('tmp.txt')
# print(Grid.read_from_file('tmp.txt', 1).start_pos)
# print(Grid.read_from_file('tmp.txt', 1).goal_pos)

