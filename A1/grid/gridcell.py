import math


class GridCell:
    """
    Based on our own (Tucker and Arthur's) A* code from RBE 3002.
    https://github.com/arthurlockman/RBE3002/blob/master/src/GridCell.py

    F(n)        = G(n)      + H(n)
    Total_cost  = to_cost   + heuristic_cost
    """
    g_val = 0

    def __init__(self, pos, goal, cell_cost, heuristic):
        self.pos = pos
        self.goal = goal
        self.cell_cost = cell_cost
        self.heuristic = heuristic
        self.__calc_heuristic__()

    def __calc_heuristic__(self):
        if self.heuristic == 1:
            self.h_val = 0
        elif self.heuristic == 2:
            self.h_val = min(abs(pos[0] - goal[0]), abs(pos[1] - goal[1]))
        elif self.heuristic == 3:
            self.h_val = max(abs(pos[0] - goal[0]), abs(pos[1] - goal[1]))
        elif self.heuristic == 4:
            self.h_val = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        elif self.heuristic == 5:
            # TODO
            pass
        else:
            # TODO
            pass

    def set_parent(self, parent_cell):
        self.parent = parent_cell
        # TODO: calculate cost to here based on parent

    def is_not_in_list(self, _list):
        # TODO
        pass
    
    def get_cell_cost(self):
        return self.cell_cost
    
    def get_x_pos(self):
        return self.pos[0]
    
    def get_y_pos(self):
        return self.pos[1]

    def get_g_val(self):
        return self.g_val
    
    def get_f_val(self):
        return self.f_val
    
    def get_h_val(self):
        return self.h_val
    
    def get_parent(self):
        return self.parent

    def set_cell_cost(self, new_cell_cost):
        self.cell_cost = new_cell_cost
    
    def get_direction_to_cell(self, goal_cell):
        difference = self - goal_cell
        dir = ''
        if difference[0] < 0:
            dir += 'S'
        elif difference[0] > 0:
            dir += 'N'
        if difference[1] < 0:
            dir += 'E'
        elif difference[1] > 0:
            dir += 'W'
        return dir
    
    def __eq__(self, other):
        return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]
    
    def __sub__(self, other):
        return self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]

    def __str__(self):
        if self.cell_cost == math.inf:
            return '#'
        else:
            return str(self.cell_cost)
    
    def __gt__(self, other):
        """
        Is this greater than another?
        """
        # TODO: Implement
        return self.get_f_val() > other.get_f_val()
    
    def __lt__(self, other):
        """
        Is this less than another?
        """
        return self.get_f_val() < other.get_f_val()

"""
Unit Tests to make sure functionality is correct
"""
g1 = GridCell([0, 0], [10, 10], 8, 1)
g2 = GridCell([10, 10], [10, 10], 8, 1)
g3 = GridCell([0, 5], [10, 10], 8, 1)
g4 = GridCell([5, 5], [10, 10], 8, 1)
assert(g1.get_direction_to_cell(g2) == 'SE')
assert(g2.get_direction_to_cell(g1) == 'NW')
assert(g3.get_direction_to_cell(g1) == 'W')
assert(g1.get_direction_to_cell(g3) == 'E')
assert(g3.get_direction_to_cell(g4) == 'S')
assert(g4.get_direction_to_cell(g3) == 'N')
assert(g1 - g2 == (-10, -10))
assert(g2 == g2)
assert(g1 != g2)

