from utils.utils import validLocation
from utils.directions import UP, DOWN, LEFT, RIGHT, getDirectionIndex

class Cell:
    def __init__(self, i, j):
        self.has_wall_up = False
        self.has_wall_left = False
        self.occupant = None
        self.position = (i, j)
        self.updateNeighbours()

    def setWalls(self, wall_up, wall_left):
        self.has_wall_left = wall_left
        self.has_wall_up = wall_up
        
    def updateNeighbours(self):
        left_location = getDirectionIndex(self.position, LEFT)
        self.neighbour_left = left_location if validLocation(*left_location) else None
        
        right_location = getDirectionIndex(self.position, RIGHT)
        self.nieghbour_right = right_location if validLocation(*right_location) else None
        
        up_location = getDirectionIndex(self.position, UP)
        self.neighbour_up = up_location if validLocation(*up_location) else None
        
        down_location = getDirectionIndex(self.position, DOWN)
        self.neighbour_down = down_location if validLocation(*down_location) else None
       
    def copy(self):
        new_cell = Cell(*self.position)
        new_cell.has_wall_up = self.has_wall_up
        new_cell.has_wall_left = self.has_wall_left
        new_cell.occupant = self.occupant  # Assuming occupant is immutable (i.e. string) or None
        return new_cell
        