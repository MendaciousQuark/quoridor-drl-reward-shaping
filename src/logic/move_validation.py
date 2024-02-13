from utils import UP, DOWN, LEFT, RIGHT, distance, validLocation
from game import Board
from errors import MoveLocationError, MoveValidationError

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
    start_cell = board[move.start[0]][move.start[1]]
    end_cell = board[move.end[0]][move.end[1]]
    
    if(move.direction not in [UP, DOWN, LEFT, RIGHT]):
        raise MoveValidationError("direction", f"Invalid direction: {move.direction}. Must be one of 'up', 'down', 'left', or 'right'. See ../utils/directions.py for more information.")
    if(end_cell.occupant != None):
        raise MoveValidationError("end", f"Invalid Move: {move.start} to {move.end}. End cell is occupied by {end_cell.occupant}. Reuest jump.")
    
    if(distance(move.start, move.end) != 1):
            return (False, f"Invalid move: {end_cell} too far")
    if(directionBlocked(move.direction, start_cell, board)):
        return (False, f"Invalid move: {end_cell} blocked by wall")
    
    return (True, "Valid move")

def validateJumpAction(move, board):
    '''
    '''
    pass

def validateWallAction(move, board):
    if(move.orientation not in ["vertical", "horizontal"]):
        raise MoveValidationError("orientation", f"Invalid orientation: {move.orientation}. Must be one of 'vertical' or 'horizontal'.")
    if(not spaceForWall(move.start, move.orientation, board)):
        return (False, f"Invalid wall placement: {move.start} {move.orientation} wall")
    
    temp_board = board.copy()
    #wants cell not move.start
    temp_board.placeWall(move.start, move.orientation)
    
        
def spaceForWall(start_cell, orientation, board):
    #if the starting location already has a wall in it return false
    if(start_cell.has_wall_up and orientation == 'horizontal'or start_cell.has_wall_left and orientation == 'vertical'):
        return False
    
    if(orientation == 'vertical'):
        last_row = 8
        first_column = 0
        cell_below = None
        cell_below_left = None
        if(start_cell[0] == last_row):
            return False
        if(start_cell[1] == first_column):
            return False
        #if there is a cell below the start cell
        if(validLocation(start_cell[0] + 1, start_cell[1])):
            cell_below = board[start_cell[0] + 1][start_cell[1]]
        #if there is a cell below and to the left of the start cell
        if(validLocation(start_cell[0] + 1, start_cell[1] - 1)):
            cell_below_left = board[start_cell[0] + 1][start_cell[1] - 1]
        #if the vertical wall passes through a horizontal wall
        if(cell_below.has_wall_up and cell_below_left.has_wall_up):
            return False
        #moving into vertical wall
        if(cell_below.has_wall_left):
            return False
        
        return True
    elif(orientation == 'horizontal'):
        last_column = 8
        first_row = 0
        cell_right = None
        cell_above_right = None
        if(start_cell[1] == last_column):
            return False
        if(start_cell[0] == first_row):
            return False
        #if there is a cell to the right of the start cell
        if(validLocation(start_cell[0], start_cell[1] + 1)):
            cell_right = board[start_cell[0]][start_cell[1] + 1]
        #if there is a cell above and to the right of the start cell
        if(validLocation(start_cell[0] - 1, start_cell[1] + 1)):
            cell_above_right = board[start_cell[0] - 1][start_cell[1] + 1]
        #if the horizontal wall passes through a vertical wall
        if(cell_right.has_wall_left and cell_above_right.has_wall_left):
            return False
        #moving into horizontal wall
        if(cell_right.has_wall_up):
            return False
        
        return True

def directionBlocked(direction, start_cell, board):
    if(direction == UP):
        if(start_cell.upWall):
            return True
    elif(direction == DOWN):
        if(board[start_cell[0] + 1][start_cell[1]].upWall):
            return True
    elif(direction == LEFT):
        if(start_cell.leftWall):
            return True
    elif(direction == RIGHT):
        if(board[start_cell[0]][start_cell[1] + 1].leftWall):
            return True
    else:
        raise MoveValidationError("direction", f"Invalid direction: {direction}. Must be one of 'up', 'down', 'left', or 'right'. See ../utils/directions.py for more information.")
