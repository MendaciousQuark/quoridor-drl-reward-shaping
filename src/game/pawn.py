import copy
from .cell import Cell


class Pawn:
    #board is a copy of the game board, colour is a bool
    def __init__(self, board, colour, i, j):
        self.colour = True if colour else False
        self.move_dir = 1 if colour else -1
        self.location = [i, j]
        self.walls = 10
    
    #def updateState
