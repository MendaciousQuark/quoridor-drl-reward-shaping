UP = (1, 0)
DOWN = (-1, 0)
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

    