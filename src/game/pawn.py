from utils import HELP_MOVE, HELP_PLACE, HELP_JUMP, HELP
from .move import Move
from logic import validateMove
from errors import MoveFormatError, MoveLocationError, MoveValidationError

class Pawn:
    #board is a copy of the game board, colour is a bool
    def __init__(self, colour, i, j):
        #'white' or 'black'
        self.colour = colour
        self.move_dir = -1 if colour == 'white' else 1
        self.position = [i, j]
        self.walls = 10
    
    def decideMoveHuman(self, board):
        move = None
        try:
            while True:
                try:
                    move = self.requestMoveInput()
                    move_valid = validateMove(move, board, self)
                    #if the move is valid, break the loop
                    if(move_valid[0]):
                        break
                    #otherwise print the error message
                    else:
                        print(move_valid[1])
                except (MoveFormatError, MoveLocationError, ValueError, MoveValidationError) as e:
                        print(e)
            if(move is None):
                raise ValueError("Move is None after validation")
            else:
                return move
        except Exception as e:
            print(e)
            print(f"An unexptected error occurred: {e}")
            raise e
               
    def requestMoveInput(self):
        print("Enter the move you would like to make. Type 'help' for a list of commands.")
        while True:
            move = input("Enter your move: ")
            print("\n")
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
                if(len(move_parts) != 4):
                    raise MoveFormatError("move", f"Invalid move: {move}\nMove should be in the format 'move direction start end'.")
                            #colour, start, end, action, direction, jumpDirection=None, orientation=None
                move = Move(self.colour, move_parts[2], move_parts[3], move_parts[0], move_parts[1], None, None)
                return move
            elif(move_parts[0] == "place" or move_parts[0] == "p"):
                #place format place orientation location
                if(len(move_parts) != 3):
                    raise MoveFormatError("place", f"Invalid place: {move}\nPlace should be in the format 'place orientation location'.")
                            #colour, start, end, action, direction, jumpDirection=None, orientation=None
                move = Move(self.colour, move_parts[2], None, move_parts[0], None, None, move_parts[1])
                return move
            elif(move_parts[0] == "jump" or move_parts[0] == "j"):
                #jump format jump start end direction
                if(len(move_parts) != 4):
                    raise MoveFormatError("jump", f"Invalid jump: {move}\nJump should be in the format 'jump start end direction'.")
                            #colour, start, end, action, direction, jumpDirection=None, orientation=None
                move = Move(self.colour, move_parts[1], move_parts[2], move_parts[0], None, move_parts[3], None)
                return move
            else:
                raise MoveFormatError("action", f"Invalid action: {move}\nAction should be one of 'move', 'place', or 'jump'. Alternatively, type 'help' for a list of commands.")
    
    def copy(self):
        return Pawn(self.colour, self.position[0], self.position[1])
    
    def __str__(self):
        return f"Pawn: {'*' if self.colour else '@'}, {self.position}, {self.walls}"
        
                