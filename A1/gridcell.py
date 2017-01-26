import math


class GridCell:
    """
    Based on our own (Tucker and Arthur's) A* code from RBE 3002.
    https://github.com/arthurlockman/RBE3002/blob/master/src/GridCell.py
    """


    def __init__(self, pos, goal, cell_cost):
        self.pos = pos
        self.goal = goal
        self.cell_cost = cell_cost
        self.explored = False
        self.directions_explored = []

    def get_position(self):
        return self.pos

    def get_goal(self):
        return self.goal

    def get_cell_cost(self):
        return self.cell_cost

    def get_row(self):
        return self.pos[0]

    def get_col(self):
        return self.pos[1]

    def is_explored(self, direction):
        return direction in self.directions_explored

    def explore(self, direction):
        self.directions_explored.append(direction)

    def set_cell_cost(self, new_cell_cost):
        self.cell_cost = new_cell_cost

    def get_direction_to_cell(self, goal_cell):
        difference = self - goal_cell
        _dir = ''
        if difference[0] < 0:
            _dir += 'S'
        elif difference[0] > 0:
            _dir += 'N'
        if difference[1] < 0:
            _dir += 'E'
        elif difference[1] > 0:
            _dir += 'W'
        return _dir

    def __eq__(self, other):
        return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]
    
    def __sub__(self, other):
        return self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]

    def write_to_string(self):
        if self.cell_cost == 10000:
            return '#'
        else:
            return str(self.cell_cost)
    
    def __gt__(self, other):
        """
        Is this greater than another?
        """
        return self.get_f_val() > other.get_f_val()
    
    def __lt__(self, other):
        """
        Is this less than another?
        """
        return self.get_f_val() < other.get_f_val()

    def __str__(self):
        return '(' + str(self.get_col()) + ', ' + str(self.get_row()) + ')'

    def __repr__(self):
        return self.__str__()

"""
Unit Tests to make sure functionality is correct
"""
g1 = GridCell([0, 0], [10, 10], 8)
g2 = GridCell([10, 10], [10, 10], 8)
g3 = GridCell([0, 5], [10, 10], 8)
g4 = GridCell([5, 5], [10, 10], 8)
assert(g1.get_direction_to_cell(g2) == 'SE')
assert(g2.get_direction_to_cell(g1) == 'NW')
assert(g3.get_direction_to_cell(g1) == 'W')
assert(g1.get_direction_to_cell(g3) == 'E')
assert(g3.get_direction_to_cell(g4) == 'S')
assert(g4.get_direction_to_cell(g3) == 'N')
assert(g1 - g2 == (-10, -10))
assert(g2 == g2)
assert(g1 != g2)
# g5 = GridCell([0, 0], [10, 10], 8)
# assert(g5.get_h_val() == 2)
# g6 = GridCell([10, 10], [0, 0], 8)
# assert(g6.get_h_val() == 1)
# g7 = GridCell([5, 5], [8, 5], 8)
# assert(g7.get_h_val() == 1)
# g8 = GridCell([5, 5], [2, 5], 8)
# assert(g8.get_h_val() == 0)



