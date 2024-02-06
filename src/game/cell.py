class Cell:
    def __init__(self, i, j):
        self.has_wall_up = False
        self.has_wall_left = False
        self.occupant = None
        self.position = (i, j)

    def setWalls(self, up, left):
        self.has_wall_left = left
        self.has_wall_up = up