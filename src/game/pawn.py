import copy
from .cell import Cell


class Pawn:
    #board is a copy of the game board, colour is a bool
    def __init__(self, board, colour):
        self.colour = True if colour else False
        
        
        