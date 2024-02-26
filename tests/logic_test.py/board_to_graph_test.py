from game.board import Board
from logic.board_to_graph import boardToGraph, cellToNode
from utils.directions import UP, DOWN, LEFT, RIGHT, getDirectionIndex

def test_boardToGraph():
    board = Board()
    board.board[4][4].has_wall_up = True
    board.board[4][4].has_wall_left = True
    graph = boardToGraph(board.board)
    
    assert len(graph) == len(board.board)
    assert len(graph[0]) == len(board.board[0])
    
    node = graph[4][4]
    assert node.position == (4, 4)
    assert node.walls == [True, True]

    neighbour_up, neighbour_left, neighbour_right, neighbour_down = defineNeighbours(node, graph)
    
    assert not neighbour_up in node.neighbours
    assert not neighbour_left in node.neighbours
    assert neighbour_down in node.neighbours
    assert neighbour_right in node.neighbours
    
    board.board[5][4].has_wall_up = True
    graph = boardToGraph(board.board)
    
    node = graph[4][4]
    assert node.position == (4, 4)
    assert node.walls == [True, True]
    
    neighbour_up, neighbour_left, neighbour_right, neighbour_down = defineNeighbours(node, graph)
    
    assert not neighbour_up in node.neighbours
    assert not neighbour_left in node.neighbours
    assert not neighbour_down in node.neighbours
    assert neighbour_right in node.neighbours
    
    node = graph[5][4]
    assert node.position == (5, 4)
    assert node.walls == [True, False]
    
    neighbour_up, neighbour_left, neighbour_right, neighbour_down = defineNeighbours(node, graph)
    
    assert not neighbour_up in node.neighbours
    assert neighbour_left in node.neighbours
    assert neighbour_down in node.neighbours
    assert neighbour_right in node.neighbours   

def defineNeighbours(node, graph):
    neighbour_up_location = getDirectionIndex(node.position, UP)
    neighbour_up = graph[neighbour_up_location[0]][neighbour_up_location[1]]
    neighbour_left_location = getDirectionIndex(node.position, LEFT)
    neighbour_left = graph[neighbour_left_location[0]][neighbour_left_location[1]]
    neighbour_right = getDirectionIndex(node.position, RIGHT)
    neighbour_right = graph[neighbour_right[0]][neighbour_right[1]]
    neighbour_down_location = getDirectionIndex(node.position, DOWN)
    neighbour_down = graph[neighbour_down_location[0]][neighbour_down_location[1]]
    
    return neighbour_up, neighbour_left, neighbour_right, neighbour_down

def test_cellToNode():
    # Create a board
    board = Board()
    #select a cell
    cell = board.board[4][4]
    # Set the walls of the cell
    cell.has_wall_up = True
    cell.has_wall_left = False
    
    #call update neighbours to ensure neighbours are updated
    cell.updateNeighbours()
    
    # Convert the cell to a node
    node = cellToNode(board.board[4][4])
    
    # Check that the node has the correct neighbours, position, and walls
    for i in range(len(cell.neighbours)):
        assert node.neighbours[i] == cell.neighbours[i]
    
    # Check that the node has the correct position and walls (up and left in that order)
    assert node.position == (4, 4)
    assert node.walls == [True, False]
