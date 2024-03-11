from models.model import Model
from game.board import Board
from game.pawn import Pawn
import pytest
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
    white_pawn = Pawn('white', 8, 4)
    black_pawn = Pawn('black', 0, 4)
    #create new models
    model_white = Model('white', white_pawn)
    model_black = Model('black', black_pawn)
    return model_white, model_black

def test_find_legal_movement(initialisedModels):
    #assign the intialised board to a variable
    board = Board()
    # assign the models to a variable
    white_model, black_model = initialisedModels
    
    #for the initial board find the legal moves for the white and black pawns
    found_moves_white = white_model.find_legal_movement(board.state, board.pawn_positions['white'])
    found_moves_black = black_model.find_legal_movement(board.state, board.pawn_positions['black'])
    
    #assert that the white pawn has 3 legal moves and the black pawn has 3 legal moves (white: up, left, right and black:down, left, right) 
    assert len(found_moves_white) == 3 == len(found_moves_black)

def test_find_legal_walls(initialisedModels):
    '''
    diff checker lives here :)
    for wall in found_walls_white:
        if wall not in found_walls_white2:
            print(wall.start, wall.orientation)
            
    '''
    #assign the intialised board to a variable
    board = Board()
    # assign the models to a variable
    white_model, black_model = initialisedModels
    
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 128 == len(found_walls_black)
    
    #place a horizontal wall in the middle of the board
    board.placeWall('horizontal', board.board[4][4])
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
        
    assert len(found_walls_white) == 124
    assert len(found_walls_black) == 124
    
    #place a vertical wall in the away from the middle and edge of the board
    board.placeWall('vertical', board.board[4][2])
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 120
    assert len(found_walls_black) == 120
    
    #place a vertical wall opposite the previous wall
    board.placeWall('vertical', board.board[4][7])
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 116
    assert len(found_walls_black) == 116
    
    #place  vertical wall near the middle of the board
    board.placeWall('vertical', board.board[4][5])
    print(board)
    found_walls_white = white_model.find_legal_walls(board.state)
    found_walls_black = black_model.find_legal_walls(board.state)
    
    assert len(found_walls_white) == 113
    assert len(found_walls_black) == 113
    