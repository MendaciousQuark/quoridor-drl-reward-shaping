from utils import moveLetterToNumber
from game import Board

def validateMove(move, board):
    if(move.action == "move"):
        return validateMoveAction(move, board)
    elif(move.action == "jump"):
        return validateJumpAction(move, board)
    elif(move.action == "place"):
        return validateWallAction(move, board)
    else:
        raise ValueError(f"Invalid action: {move.action}. Must be one of 'move', 'jump', or 'place'.")

def validateMoveAction(move, board):
    '''
    is direction UP, down, left, right?
        is move off the board?
            return (false, 'invalid move: off the board')
        is target more than 1 away?
            return (false, 'invalid move: too far')
        is the cell in direction occupied by pawn?
            raise error wrong move format : request jump
        is move diagonal?
            return (false, 'invalid move: diagonal')
        is the cell in direction blocked by wall?
            return (false, 'invalid move: blocked by wall')
        else:
            return (true, 'valid move')
    else:
        raise error unknown direction
    '''
    pass

def validateJumpAction(move, board):
    '''
    '''
    pass

def validateWallAction(move, board):
    pass


