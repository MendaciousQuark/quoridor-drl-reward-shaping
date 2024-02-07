class Cell:
    def __init__(self, i, j):
        self.has_wall_up = False
        self.has_wall_left = False
        self.occupant = None
        self.position = (i, j)

    def setWalls(self, up, left):
        self.has_wall_left = left
        self.has_wall_up = up
        
    def copy(self):
        new_cell = Cell(*self.position)
        new_cell.has_wall_up = self.has_wall_up
        new_cell.has_wall_left = self.has_wall_left
        new_cell.occupant = self.occupant  # Assuming occupant is immutable (i.e. string) or None
        return new_cell
        