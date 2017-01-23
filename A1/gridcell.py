class GridCell:
    """
    Based on our own (Tucker and Arthur's) A* code from RBE 3002.
    https://github.com/arthurlockman/RBE3002/blob/master/src/GridCell.py
    """
    Gval = 0

    def __init__(self, x, y, occupancyLevel, heuristic):
        self.Xpos = x
        self.Ypos = y
        self.occupancyLevel = occupancyLevel
        self.heuristic = heuristic

        if 30 >= occupancyLevel:
            self.empty = True
        else:
            self.empty = False

    def setH(self, goalX, goalY):
        if self.heuristic == 1:
            return 1
        # TODO: Calculate each of the different heuristics

    def setParent(self, parentCell):
        self.parent = parentCell
        # TODO: calculate cost to here based on parent

    def isNotInList(self, _list):
        for cell in _list:
            if cell.getXpos() == self.Xpos and cell.getYpos() == self.Ypos:
                return false
        return True
    
    def isEmpty(self):
        return self.empty
    
    def getXpos(self):
        return self.Xpos
    
    def getYpos(self):
        return self.Ypos

    def getGval(self):
        return self.Gval
    
    def getFval(self):
        return self.Fval
    
    def getHval(self):
        return self.Hval
    
    def getParent(self):
        return self.parent
    
    def getOccupancyLevel(self):
        return self.occupancyLevel
    
    def setOccupancyLevel(self, occupancyval):
        self.occupancyLevel = occupancyval
        # TODO: calculate empty vs non empty
    
    def __eq__(self, other):
        return self.Xpos == other.Xpos and self.Ypos = other.Ypos
    
