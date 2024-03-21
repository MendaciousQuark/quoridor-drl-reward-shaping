from logic.a_star import aStar, setheuristicCost, aStar_without_priority_queue
from logic.board_to_graph import boardToGraph
from game.board import Board
import time
import random
import pytest

def test_aStar():
    graph = boardToGraph(Board().board)
    #set white goal
    white_goal = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
    #set black goal
    black_goal = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
    
    #test for the white player wiht nothing on the board
    path = aStar(graph, 'white', (8, 4), white_goal)
    assert path == [(8, 4), (7, 4), (6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4)]
    
    #use new board (without seems to cause undefined behaviour in the tests)
    graph = boardToGraph(Board().board)
    
    #test for the black player with nothing on the board
    path = aStar(graph, 'black', (0, 4), black_goal)
    assert path == [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4)]
    
    #initialise new boards (this time with walls)
    board_with_path, board_without_path = setNewBoards()
    
    for colour in ['white', 'black']:
        graph = boardToGraph(board_with_path.board)
        
        #test for current colour
        start = (8, 4) if colour == 'white' else (0, 4)
        goal = white_goal if colour == 'white' else black_goal
        path = aStar(graph, colour, start, goal)
        print(board_with_path)
        print(path)
        if(colour == 'white'):
            assert (8, 4) in path
            assert (6, 4) in path or (8, 8) in path # both ptions have same path length so depends on heuristic
            assert (8, 5) in path or (7, 4) in path # same as above
            assert (2, 6) in path
            assert (0, 6) in path
        else:
            assert (0, 4) in path
            assert (1, 6) in path or (0, 6) in path
            assert (3, 8) in path
            assert (8, 8) in path
            
        graph = boardToGraph(board_without_path.board)
        start = (8, 4) if colour == 'white' else (0, 4)
        goal = white_goal if colour == 'white' else black_goal
        path = aStar(graph, colour, start, goal)
        
        assert path == []
    
def setNewBoards():
    board_with_path = Board()
    
    #place walls to force a complex path
    board_with_path.placeWall('horizontal', board_with_path.board[4][0])
    board_with_path.placeWall('horizontal', board_with_path.board[4][2])
    board_with_path.placeWall('horizontal', board_with_path.board[4][4])
    board_with_path.placeWall('horizontal', board_with_path.board[4][6])
    board_with_path.placeWall('horizontal', board_with_path.board[2][7])
    board_with_path.placeWall('vertical', board_with_path.board[0][7])
    board_with_path.placeWall('vertical', board_with_path.board[2][6])
    board_with_path.placeWall('vertical', board_with_path.board[4][8])
    
    #initialise a new board
    board_without_path = Board()
    
    #place walls to block all paths
    board_without_path.placeWall('horizontal', board_without_path.board[4][0])
    board_without_path.placeWall('horizontal', board_without_path.board[4][2])
    board_without_path.placeWall('horizontal', board_without_path.board[4][4])
    board_without_path.placeWall('horizontal', board_without_path.board[4][6])
    board_without_path.placeWall('horizontal', board_without_path.board[2][7])
    board_without_path.placeWall('vertical', board_without_path.board[2][7])
    board_without_path.placeWall('vertical', board_without_path.board[4][2])
    board_without_path.placeWall('vertical', board_without_path.board[4][3])
    
    return board_with_path, board_without_path

def test_setHeuristicCost():
    graph = boardToGraph(Board().board)
    #set the heuristic cost for the white player
    setheuristicCost(graph, 'white')
    for i, row in enumerate(graph):
        for j, node in enumerate(row):
            print('row:', i, 'col:', j, 'heuristic:', node.heuristic_cost, 'position:', node.position)
            assert node.heuristic_cost == node.position[0]
    
    #set the heuristic cost for the black player
    setheuristicCost(graph, 'black')
    for i, row in enumerate(graph):
        for j, node in enumerate(row):
            assert node.heuristic_cost == 8 - node.position[0]

@pytest.mark.slow
def test_performance():
    # Initialize variables to store execution times
    execution_time_with_pq = 0
    execution_time_without_pq = 0

    #goals
    #set white goal
    white_goal = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
    #set black goal
    black_goal = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
    

    # Create a list of random boards to test
    number_of_boards = 1000
    boards_to_test = [creatRandomBoard() for _ in range(number_of_boards)]
    print('Number of boards created:', number_of_boards)
    # turn each board into a graph
    white_positions = [board[1]['white'] for board in boards_to_test]
    black_positions = [board[1]['black'] for board in boards_to_test]
    graphs = [boardToGraph(board[0].board) for board in boards_to_test]
    print('Graphs created.')
    # Test the performance of A* with a priority queue
    print('Starting tests...')
    print('Testing with priority queue...')
    start_time = time.time()
    for i in range(number_of_boards):
        #perform a* for white or black at random
        colour = 'white' if random.choice([True, False]) else 'black'
        start = white_positions[i] if colour == 'white' else black_positions[i]
        goal = white_goal if colour == 'white' else black_goal
        aStar(graphs[i], colour, start, goal)
    #avrage execution time with priority queue
    execution_time_with_pq = (time.time() - start_time)/number_of_boards
    print('Execution time with priority queue:', execution_time_with_pq)
    
    #need to turn boards into graphs again as they were modified by the previous tests (positions stayed the same)
    graphs = [boardToGraph(board[0].board) for board in boards_to_test]
    
    print('Testing without priority queue...')
    # Test the performance of A* without a priority queue
    start_time = time.time()
    for i, board in enumerate(boards_to_test):
        #perform a* for white or black at random
        colour = 'white' if random.choice([True, False]) else 'black'
        start = white_positions[i] if colour == 'white' else black_positions[i]
        goal = white_goal if colour == 'white' else black_goal
        aStar_without_priority_queue(graphs[i], colour, start, goal)
    #avrage execution time without priority queue
    execution_time_without_pq = (time.time() - start_time)/number_of_boards
    print('Execution time without priority queue:', execution_time_without_pq)

    # Print the execution times
    print('\nExecution time with priority queue:', execution_time_with_pq)
    print('Execution time without priority queue:', execution_time_without_pq)

    # Assert that the version with the priority queue is faster
    assert execution_time_with_pq < execution_time_without_pq, "A* with priority queue should be faster than without"

def creatRandomBoard():
    #remove all pawns
    board = Board()
    board.removePawns()
    number_of_walls = random.randint(0, 10)
    for i in range(number_of_walls):
        while True:
            try:
                #choose a random wall type
                wall_type = random.choice(['horizontal', 'vertical'])
                #choose a random cell that is not at the edge of the board
                cell_location = random.choice([(random.randint(1, 7), random.randint(0, 8)), (random.randint(0, 8), random.randint(1, 7))])
                cell = board.board[cell_location[0]][cell_location[1]]
                board.placeWall(wall_type, cell)
                break
            except Exception as e:
                continue
    
    #place pawns randomly
    #white shouldn't be on row 0
    board.pawn_positions['white'] = [random.randint(1, 8), random.randint(0, 8)]
    #black shouldn't be on row 8
    board.pawn_positions['black'] = [random.randint(0, 7), random.randint(0, 8)]
    board.placePawns()
    #chose a random even or odd number betweeen 0 and 11
    board.turn = random.choice([0, 11])
    board.updateState()
    
    #return a list containing the board and the pawn positions
    return [board, board.pawn_positions]