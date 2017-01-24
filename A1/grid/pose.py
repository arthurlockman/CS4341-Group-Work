
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