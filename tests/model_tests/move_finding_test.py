from models.model import Model
from game.board import Board
from game.pawn import Pawn
import pytest
import pdb
import timeit
'''
        Example board
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   | @ |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+=======+---+---+---+
        # |   |   #   |   |   |   |   |   |   |
        # +-------#---+---+---+---+---+---+---+
        # |   |   #   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   | * |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        
        non-edge horizontal wall removes: 1 vertical and 3 horizontal walls (itself one to the left and one to the right)
        edge horizontal wall removes: 1 vertical and 2 horizontal walls (itself and one to the side away from the edge)
        non-edge vertical wall removes: 3 vertical and 1 horizontal walls (itself and one above and one below)
        edge vertical wall removes: 2 vertical and 1 horizontal walls (itself and one away from the edge)
        
'''
#create a model object before each test
@pytest.fixture(autouse=True)
def initialisedModels():
    #creae a pawn object for the white and black pawns
    pawns = {'white': Pawn('white', 8, 4), 'black': Pawn('black', 0, 4)}

    #create new models
    model_white = Model('white', pawns)
    model_black = Model('black', pawns)
    return model_white, model_black

def test_find_legal_movement(initialisedModels):
    #assign the intialised board to a variable
    board = Board()
    # assign the models to a variable
    white_model, black_model = initialisedModels
    
    #for the initial board find the legal moves for the white and black pawns
    # found_moves_white = white_model.find_legal_movement(board.state, board.pawn_positions['white'])
    # board.turn = 1
    # board.updateState()
    # found_moves_black = black_model.find_legal_movement(board.state, board.pawn_positions['black'])
    
    # #assert that the white pawn has 3 legal moves and the black pawn has 3 legal moves (white: up, left, right and black:down, left, right) 
    # assert len(found_moves_white) == 3 == len(found_moves_black)
    # #codes for up, down, left, right : 0, 1, 2, 3
    # for move in found_moves_white:
    #     assert move[1] == 0 or move[1] == 2 or move[1] == 3
    # for move in found_moves_black:
    #     assert move[1] == 1 or move[1] == 2 or move[1] == 3
    
    # for move in found_moves_white:
    #     #jumps should be impossible (4-6 are the ids for jumping)
    #     assert move[1] != 4 and move[1] != 5 and move[1] != 6
        
    # #use a new board
    # board = Board()
    
    # #place pawns next to each other
    # board.removePawns()
    # board.pawn_positions['white'] = [4, 4]
    # board.pawn_positions['black'] = [4, 5]
    # board.placePawns()
    # board.updateState()
    
    # #find the legal moves for the white and black pawns
    # pdb.set_trace()
    # found_moves_white = white_model.find_legal_movement(board.state, board.pawn_positions['white'])
    # found_moves_black = black_model.find_legal_movement(board.state, board.pawn_positions['black'])
    
    # #white should have m,oves 0, 1, 2, 6
    # print(board)
        
    # for move in found_moves_white:
    #     assert move[1] == 0 or move[1] == 1 or move[1] == 2 or move[1] == 6
    # #black should have moves 0, 1, 3, 6
    # for move in found_moves_black:
    #     assert move[1] == 0 or move[1] == 1 or move[1] == 3 or move[1] == 6
        
    # #use a new board
    # board = Board()
    
    # #place pawns next to each other
    # board.removePawns()
    # board.pawn_positions['white'] = [4, 4]
    # board.pawn_positions['black'] = [4, 5]
    # board.placePawns()
    
    # #place a vertical wall behind each pawn
    # board.placeWall('vertical', board.board[4][4])
    # board.placeWall('vertical', board.board[4][6])
    
    # board.updateState()
    
    # #find the legal moves for the white and black pawns
    # # pdb.set_trace()
    # found_moves_white = white_model.find_legal_movement(board.state, board.pawn_positions['white'])
    # found_moves_black = black_model.find_legal_movement(board.state, board.pawn_positions['black'])
    
    # print(board)
    
    # #legal moves for white up down jump right and jump left = 0, 1, 3, 4
    # for move in found_moves_white:
    #     assert move[1] == 0 or move[1] == 1 or move[1] == 3 or move[1] == 4
    # #legal moves for black up down jump right and jump left = 0, 1, 2, 5
    # for move in found_moves_black:
    #     assert move[1] == 0 or move[1] == 1 or move[1] == 2 or move[1] == 5
    
    # #use a new board
    # board = Board()
    
    # #place pawns next to each other
    # board.removePawns()
    # board.pawn_positions['white'] = [4, 4]
    # board.pawn_positions['black'] = [3, 4]
    # board.placePawns()
    
    # #put them in a 'tunnel' with vertical walls so they have to jump over each other or move away from each other
    # board.placeWall('vertical', board.board[4][4])
    # board.placeWall('vertical', board.board[4][5])
    # board.placeWall('vertical', board.board[2][4])
    # board.placeWall('vertical', board.board[2][5])
    # board.updateState()
    
    # #find the legal moves for the white and black pawns
    # found_moves_white = white_model.find_legal_movement(board.state, board.pawn_positions['white'])
    # found_moves_black = black_model.find_legal_movement(board.state, board.pawn_positions['black'])
    
    # print(board)
        
    # #legal moves fro white are straight jump up and move down = 1, 6
    # assert len(found_moves_white) == 2
    # for move in found_moves_white:
    #     assert move[1] == 1 or move[1] == 6
    # #legal moves for black are straight jump down and move up = 0, 6
    # assert len(found_moves_black) == 2
    # for move in found_moves_black:
    #     assert move[1] == 0 or move[1] == 6
    
    #use a new board
    board = Board()
    
    #place pawns next to each other at the edge of the board
    board.removePawns()
    board.pawn_positions['white'] = [7, 7]
    board.pawn_positions['black'] = [7, 8]
    board.placePawns()
    
    #encase the pawns with walls so that the only exit is up for black
    board.placeWall('horizontal', board.board[7][6])
    board.placeWall('horizontal', board.board[8][7])
    board.placeWall('vertical', board.board[7][7])
    
    board.updateState()
    
    #find the legal moves for the white and black pawns
    found_moves_white = white_model.find_legal_movement(board.state, board.pawn_positions['white'])
    found_moves_black = black_model.find_legal_movement(board.state, board.pawn_positions['black'])
    
    print(board)
    
    #legal move for white is jump left/up = 4
    assert len(found_moves_white) == 1
    for move in found_moves_white:
        assert move[1] == 4
    #legal move for black is move up = 1
    assert len(found_moves_black) == 1
    for move in found_moves_black:
        assert move[1] == 0

    
def test_find_legal_walls(initialisedModels):
    '''
    diff checker lives here :)
    for wall in found_walls_white:
        if wall not in found_walls_white2:
            print(wall[1], wall[0].start, wall[0].orientation)
            
    '''
    #assign the intialised board to a variable
    board = Board()
    # assign the models to a variable
    white_model, black_model = initialisedModels
    
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 128 
    assert len(found_walls_black) == 128
    
    #place a horizontal wall in the middle of the board
    board.placeWall('horizontal', board.board[4][4])
    board.updateState()
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
      
    assert len(found_walls_white) == 124
    assert len(found_walls_black) == 124
    
    #place a vertical wall in the away from the middle and edge of the board
    board.placeWall('vertical', board.board[4][2])
    board.updateState()
    print(board)
    found_walls_white2 = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    for wall in found_walls_white:
        if wall not in found_walls_white2:
            print(wall[1], wall[0].start, wall[0].orientation)
    
    assert len(found_walls_white2) == 120
    assert len(found_walls_black) == 120
    
    #place a vertical wall opposite the previous wall
    board.placeWall('vertical', board.board[4][7])
    board.updateState()
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 116
    assert len(found_walls_black) == 116
    
    #place  vertical wall near the middle of the board
    board.placeWall('vertical', board.board[4][5])
    board.updateState()
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 113
    assert len(found_walls_black) == 113
            
    #place horizontal board at the right edge of the board
    board.placeWall('horizontal', board.board[4][7])
    board.updateState()
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 110
    assert len(found_walls_black) == 110
    
    #place horizontal to adjacent to middle horizontal wall
    board.placeWall('horizontal', board.board[4][2])
    board.updateState()
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 106
    assert len(found_walls_black) == 106

def test_timed_find_legal_walls(initialisedModels):
    # Assign the initialised board to a variable
    board = Board()
    # Assign the models to a variable
    white_model, black_model = initialisedModels

    # Prepare the context for timeit
    context = globals().copy()  # Copy the global context
    context.update({
        'white_model': white_model,
        'black_model': black_model,
        'board': board  # Ensure 'board' is also included if it's referenced
    })

    # Define the code to test as strings
    iterations = 1
    time_test_1 = 'white_model.find_legal_walls(board.state)'
    times_one = timeit.timeit(time_test_1, globals=context, number=iterations)
    print(f"Time taken for 1000 iterations of {time_test_1}: {times_one}")
    
    # time_test_2 = 'black_model.find_legal_walls(board.state)'
    # times_two = timeit.timeit(time_test_2, globals=context, number=iterations)
    # print(f"Time taken for 1000 iterations of {time_test_2}: {times_two}")
    
    # Perform assertions
    assert times_one/iterations < 0.5, f"white_model.find_legal_walls took too long: {times_one}s"
    #assert times_two < 0.1, f"black_model.find_legal_walls took too long: {times_two}s"
