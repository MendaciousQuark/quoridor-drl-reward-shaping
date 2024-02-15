import copy
from .cell import Cell
from utils import HELP_MOVE, HELP_PLACE, HELP_JUMP, HELP
from .move import Move
from errors import MoveFormatError, MoveLocationError

class Pawn:
    #board is a copy of the game board, colour is a bool
    def __init__(self, board, colour, i, j):
        self.colour = colour
        self.move_dir = 1 if colour else -1
        self.location = [i, j]
        self.walls = 10
    
    def makeMoveHuman(self):
        pass
            
    def rquestMoveInput(self):
        print("Enter the move you would like to make. Type 'help' for a list of commands.")
        try:
            while True:
                try:
                    move = input("Enter your move: ")
                    move_parts = move.split()
                    if(move_parts[0] == "help"):
                        if(len(move_parts) == 1):
                            print(HELP)
                        elif(move == "help move"):
                            print(HELP_MOVE)
                        elif(move == "help place"):
                            print(HELP_PLACE)
                        elif(move == "help jump"):
                            print(HELP_JUMP)
                    elif(move_parts[0] == "move" or move_parts[0] == "m"):
                        #move format move direction start end
                                    #colour, start, end, action, direction, jumpDirection=None, orientation=None
                        move = Move(self.colour, move_parts[2], move_parts[3], move_parts[0], move_parts[1])
                        return move
                    elif(move_parts[0] == "place" or move_parts[0] == "p"):
                        #place format place orientation location
                                    #colour, start, end, action, direction, jumpDirection=None, orientation=None
                        move = Move(self.colour, move_parts[2], None, move_parts[0], None, None, move_parts[1])
                        return move
                    elif(move_parts[0] == "jump" or move_parts[0] == "j"):
                        #jump format jump start end direction
                                    #colour, start, end, action, direction, jumpDirection=None, orientation=None
                        move = Move(self.colour, move_parts[1], move_parts[2], move_parts[0], None, move_parts[3], None)
                        return move
                except (MoveFormatError, MoveLocationError) as e:
                    print(e)
        except Exception as e:
            print(f"An unexptected error occurred: {e}")
                