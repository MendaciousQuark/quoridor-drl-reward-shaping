from utils import validLocation, locationToCell, boardToGraph, opposingPawnAdjacent
from utils.directions import *
from errors import MoveLocationError, MoveValidationError
from .a_star import aStar

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
    if(move.jumpDirection is None):
        raise MoveValidationError("jumpDirection", f"Invalid jump: {move.start} to {move.end}. No jump direction provided.")
    elif(move.jumpDirection not in [UP, DOWN, LEFT, RIGHT]):
        raise MoveValidationError("jumpDirection", f"Invalid jump direction: {move.jumpDirection}. Must be one of 'up', 'down', 'left', or 'right'. See ../utils/directions.py for more information.")
    #check for adjacent opposing pawn
    adjacent_pawn = opposingPawnAdjacent(move.colour, board, locationToCell(move.start[0], move.start[1], board))
    if(adjacent_pawn[0] == False):
        return (False, f"Invalid jump: {move.start} to {move.end}. No adjacent opposing pawn.")
    
    #determine the direction of 
    base_direction = UP if move.colour == "white" else DOWN
    start_cell = locationToCell(move.start[0], move.start[1], board)
    #if there is no wall behind opposing pawn in the direction of the jump but a diagonal jump is requested
    straight_jump_blocked = straightJumpBlocked(start_cell, board, adjacent_pawn, move)
    if(straight_jump_blocked):
        if(not validAlternateJumpDirection(start_cell, board, adjacent_pawn, move)):
            return (False, f"Invalid jump: {move.start} to {move.end}. Jump direction not valid or blocked by wall.")
        else:
            if(distance(move.start, move.end) != 1):
                return (False, f"Invalid jump: {move.start} to {move.end}. Diagonal jump distance must be 1.")
            else:
                return (True, "Valid jump")
    elif(not straight_jump_blocked):
        if(distance(move.start, move.end) != 2):
            return (False, f"Invalid jump: {move.start} to {move.end}. Straight jump distance must be 2.")
        else:
            return (True, "Valid jump")
    
def straightJumpBlocked(start_cell, board, adjacent_pawn, move):
    adjacent_pawn_direction = getCellDirection(adjacent_pawn[1], start_cell)

    if(move.jumpDirection == adjacent_pawn_direction):
        return directionBlocked(move.jumpDirection, adjacent_pawn[1], board)
    else:
        return False
#assuming straight jump over opponent not possible
def validAlternateJumpDirection(start_cell, board, adjacent_pawn, move):
    adjacent_pawn_direction = getCellDirection(adjacent_pawn[1], start_cell)
    jump_target_location = None
    #determine the jump target location (adjusting for orientation of adjacent pawn)
    if (adjacent_pawn_direction == UP):
        jump_target_location = getDirectionIndex(adjacent_pawn[1], LEFT) if(move.jumpDirection == LEFT) else getDirectionIndex(adjacent_pawn[1], RIGHT)
    elif (adjacent_pawn_direction == DOWN):
        jump_target_location = getDirectionIndex(adjacent_pawn[1], RIGHT) if(move.jumpDirection == LEFT) else getDirectionIndex(adjacent_pawn[1], LEFT)
    elif (adjacent_pawn_direction == LEFT):
        jump_target_location = getDirectionIndex(adjacent_pawn[1], DOWN) if(move.jumpDirection == LEFT or move.jumpDirection == DOWN) else getDirectionIndex(adjacent_pawn[1], UP)
    elif (adjacent_pawn_direction == RIGHT):
        jump_target_location = getDirectionIndex(adjacent_pawn[1], UP) if(move.jumpDirection == LEFT or move.jumpDirection == UP) else getDirectionIndex(adjacent_pawn[1], DOWN)
    else:
        raise ValueError(f"Invalid adjacent pawn direction: {adjacent_pawn_direction}. Must be one of 'up', 'down', 'left', or 'right'.")
    
    #if the target location is not valid
    if(not validLocation(*jump_target_location)):
        return False
    
    #convert the target location to a cell
    jump_target_cell = locationToCell(*jump_target_location, board)
    #get the direction to the target cell from the adjacent pawn cell
    jump_direction = getCellDirection(jump_target_cell, adjacent_pawn[1])
    if(directionBlocked(jump_direction, adjacent_pawn[1], board)):
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

def validateWallAction(move, board):
    if(move.orientation not in ["vertical", "horizontal"]):
        raise MoveValidationError("orientation", f"Invalid orientation: {move.orientation}. Must be one of 'vertical' or 'horizontal'.")
    if(not spaceForWall(move.start, move.orientation, board)):
        return (False, f"Invalid wall placement: {move.start} {move.orientation} wall")
    
    temp_board = board.copy()
    
    try:
        start_cell =  locationToCell(move.start[0], move.start[1], temp_board)
    except ValueError:
        raise MoveLocationError("start", f"Invalid start location: {move.start}. Must be in the range (0, 0) to (8, 8).")
    
    temp_board.placeWall(start_cell, move.orientation)
    graph_board = boardToGraph(temp_board)
    goal = temp_board[0] if move.colour == "white" else temp_board[8]
    path_to_goal = aStar(graph_board, move.colour, temp_board, goal)
    if(len(path_to_goal) == 0):
        return (False, f"Invalid wall placement: {move.start} {move.orientation} wall blocks path")
    else:
        return (True, "Valid wall placement")
        
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
