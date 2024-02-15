# Import necessary modules and classes
from .node import Node
from utils import validLocation, UP, DOWN, LEFT, RIGHT, getDirectionIndex

#boardToGraph function converts a game board to a graph
def boardToGraph(board):
    # Calculate the dimensions of the board
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    
    # Initialize an empty graph with the same dimensions as the board
    graph = [[None for _ in range(width)] for _ in range(height)]
    
    # Convert each cell in the board to a Node and store it in the graph
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            graph[i][j] = cellToNode(cell)
    
    # Update the neighbors for each node in the graph based on walls and valid movements
    for i, row in enumerate(graph):
        for j, node in enumerate(row):
            updated_neighbours = []  # Temporary list to hold valid neighbors
            for neighbour_pos in node.neighbours:
                # Ensure the neighbor position is not None and is valid
                if neighbour_pos is not None and validLocation(*neighbour_pos):
                    can_move = True  # Flag to check if movement is possible
                    # Check each direction and validate movement based on walls
                    if(neighbour_pos == tuple(getDirectionIndex(node.position, UP)) and node.walls[0]):
                        can_move = False
                    elif(neighbour_pos == tuple(getDirectionIndex(node.position, DOWN)) and graph[node.position[0] + 1][node.position[1]].walls[0]):
                        can_move = False
                    elif(neighbour_pos == tuple(getDirectionIndex(node.position, LEFT)) and node.walls[1]):
                        can_move = False
                    elif(neighbour_pos == tuple(getDirectionIndex(node.position, RIGHT)) and graph[node.position[0]][node.position[1] + 1].walls[1]):
                        can_move = False
                        
                    # If movement is allowed, add the neighbor to the updated list
                    if can_move:
                        updated_neighbours.append(graph[neighbour_pos[0]][neighbour_pos[1]])
                    # If the position is invalid (off the board), raise an error
                    else:
                        raise ValueError(f"Invalid neighbour position: {neighbour_pos}. Must be on the board.")
                        
            # Replace the node's neighbors with the updated list of valid neighbors
            node.neighbours = updated_neighbours
    return graph

def cellToNode(cell):
    # Filter out None values from the cell's neighbors and return a new Node
    neighbours = [neighbour for neighbour in cell.neighbours if neighbour is not None]
    position = cell.position
    walls = [cell.has_wall_up, cell.has_wall_left]
    return Node(neighbours, position, walls)
