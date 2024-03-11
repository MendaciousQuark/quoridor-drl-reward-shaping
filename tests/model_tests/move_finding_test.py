from models.model import Model
from game.board import Board
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
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   | * |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
'''
#create a model object before each test
@pytest.fixture(autouse=True)
def initialisedModels():
    #create a new board and return it
    model_white = Model('white')
    model_black = Model('black')
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

def test_find_legal_walls():
    pass