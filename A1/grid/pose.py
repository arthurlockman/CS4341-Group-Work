from gridcell import GridCell

class Pose:
    """
    F(n)        = G(n)      + H(n)
    Total_cost  = to_cost   + heuristic_cost
    """

    g_val = 0
    
    def __init__(self, gridcell, direction, heuristic):
        self.gridcell = gridcell
        self.direction = direction
        self.heuristic = heuristic
        self.__calc_heuristic__()

    def __calc_heuristic__(self):
        goal = self.gridcell.get_goal()
        pos = self.gridcell.get_position()
        if self.heuristic == 1:
	        self.h_val = 0
        elif self.heuristic == 2:
            self.h_val = min(abs(pos[0] - goal[0]), abs(pos[1] - goal[1]))
        elif self.heuristic == 3:
            self.h_val = max(abs(pos[0] - goal[0]), abs(pos[1] - goal[1]))
        elif self.heuristic == 4:
            self.h_val = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        elif self.heuristic == 5:
            goalcell = GridCell(goal, goal, 0)
            dir_to_goal = self.gridcell.get_direction_to_cell(goalcell)
            if len(dir_to_goal) == 1:
                self.h_val = 1
            elif len(dir_to_goal) == 2:
                self.h_val = 2
            if self.direction in dir_to_goal:
                self.h_val -= 1
        else:
	        # TODO
	        pass

    def set_parent(self, parent_pose, edge_cost):
        self.parent = parent_pose
        
        f_val = parent_pose.get_f_val() + edge_cost + self.h_val()
    
    def get_g_val(self):
        return self.g_val
    
    def get_f_val(self):
        return self.f_val
    
    def get_h_val(self):
        return self.h_val
    
    def get_parent(self):
        return self.parent

    def get_position(self):
        return self.gridcell.get_position()

    def get_direction(self):
           return self.direction

    def get_heuristic(self):
        return self.heuristic

g1 = GridCell([0, 0], [10, 10], 8)
g2 = GridCell([10, 10], [0, 0], 8)
g3 = GridCell([5, 5], [8, 5], 8)
g4 = GridCell([5, 5], [2, 5], 8)

p1 = Pose(g1, 'N', 5)
p2 = Pose(g2, 'N', 5)
p3 = Pose(g3, 'N', 5)
p4 = Pose(g4, 'N', 5)

assert(p1.get_h_val() == 2)
assert(p2.get_h_val() == 1)
assert(p3.get_h_val() == 1)
assert(p4.get_h_val() == 0)
