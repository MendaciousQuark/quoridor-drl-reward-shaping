#directions are inverted since Up for us (humans) is down in an array
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def getDirectionIndex(position, direction):
    # Check if 'position' and 'direction' are tuples/lists of length 2 and contain only integers
    if not (isinstance(position, (tuple, list)) and len(position) == 2 and all(isinstance(i, int) for i in position)):
        raise ValueError("position must be a tuple or list of two integers")
    
    if not (isinstance(direction, (tuple, list)) and len(direction) == 2 and all(isinstance(i, int) for i in direction)):
        raise ValueError("direction must be a tuple or list of two integers")
    
    # Return a list containing the position after moving one step in 'direction'
    return [position[0] + direction[0], position[1] + direction[1]]

def getCellDirection(target_cell, start_cell):
    if target_cell.position[0] == start_cell.position[0] - 1:
        return UP
    elif target_cell.position[0] == start_cell.position[0] + 1:
        return DOWN
    elif target_cell.position[1] == start_cell.position[1] - 1:
        return LEFT
    elif target_cell.position[1] == start_cell.position[1] + 1:
        return RIGHT
    else:
        raise ValueError(f"Invalid target cell: {target_cell}. Must be adjacent to start cell: {start_cell} (can not be diagonal).")
    
#look over logic of function
def distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])
    