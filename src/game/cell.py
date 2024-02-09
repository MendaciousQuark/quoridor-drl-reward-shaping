from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, validLocation

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
        self.neighbour_right = right_location if validLocation(*right_location) else None
        
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
    
    def __str__(self):
        walls = "".join(["U" if self.has_wall_up else "",
                        "L" if self.has_wall_left else ""])
        
        occupant_str = str(self.occupant) if self.occupant is not None else ""
        
        neighbours = "".join(["U" if self.neighbour_up else "",
                            "D" if self.neighbour_down else "",
                            "L" if self.neighbour_left else "",
                            "R" if self.neighbour_right else ""])
        
        # Check if any information is present
        if walls or occupant_str or neighbours:
            return f"Walls: {walls}\n" \
                f"Position: {self.position}\n" \
                f"Occupant: {occupant_str}\n" \
                f"Neighbours: {neighbours}\n"
        else:
            return f"Position: {self.position}"


        