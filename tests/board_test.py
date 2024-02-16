from src.game.board import Board, Cell
from tests.test_utils import *
import pytest, random

@pytest.fixture(autouse=True)
def intialisedBoard():
    board = Board()
    return board

def test_initBoard(intialisedBoard):
    board = intialisedBoard
    start_test_board = [[Cell(i, j) for j in range(9)] for i in range(9)]
    start_test_board[0][4].occupant = "black"
    start_test_board[8][4].occupant = "white"
    assert board.board == start_test_board
    
def test_printBoard(intialisedBoard, capsys):
    board = intialisedBoard
    print(board.printBoard())
    captured = capsys.readouterr()
    expected_output = INIT_BOARD
    assert captured.out == expected_output

def test_placeWall(intialisedBoard, capsys):
    #assign the board to a variable
    board = intialisedBoard
    #place a wall
    board.placeWall("horizontal", board.board[8][3])
    #print the board
    print(board.printBoard())
    #capture the output
    captured = capsys.readouterr()
    #define the expected output
    expected_output = PLACE_WALL_HORIZONTAL
    
    assert captured.out == expected_output
    
    #place a vertical wall
    board.placeWall("vertical", board.board[7][3])
    
    
    #capture the output
    captured = capsys.readouterr()
    #define the expected output
    expected_output = PLACE_WALL_HORIZONTAL_THEN_VERTICAL

def test_move(intialisedBoard, capsys):
    board = intialisedBoard
    
    #move the black piece to the right
    board.movePawn(False, board.board[0][5].position)
    print(board.printBoard())
    #capture the output
    captured_black_move_right = capsys.readouterr()
    
    #move black piece down
    board.movePawn(False, board.board[1][5].position)
    print(board.printBoard())
    #capture the output
    captured_black_move_down = capsys.readouterr()
    
    #move black piece up
    board.movePawn(False, board.board[0][5].position)
    print(board.printBoard())
    #capture the output
    captured_black_move_up = capsys.readouterr()
    
    #move black piece to the left
    board.movePawn(False, board.board[0][4].position)
    print(board.printBoard())
    #capture the output
    captured_black_move_left = capsys.readouterr()
    
    #move white piece to the right
    board.movePawn(True, board.board[8][3].position)
    print(board.printBoard())
    #capture the output
    captured_white_move_left = capsys.readouterr()
    
    #move white piece to the right
    board.movePawn(True, board.board[8][4].position)
    print(board.printBoard())
    #capture the output
    captured_white_move_right = capsys.readouterr()
    
    #move white piece up
    board.movePawn(True, board.board[7][4].position)
    print(board.printBoard())
    #capture the output
    captured_white_move_up = capsys.readouterr()
    
    #move white piece down
    board.movePawn(True, board.board[8][4].position)
    print(board.printBoard())
    #capture the output
    captured_white_move_down = capsys.readouterr()
    
    assert captured_black_move_right.out == MOVE_BLACK_RIGHT
    assert captured_black_move_down.out == MOVE_BLACK_DOWN
    assert captured_black_move_up.out == MOVE_BLACK_UP
    assert captured_black_move_left.out == MOVE_BLACK_LEFT
    assert captured_white_move_left.out == MOVE_WHITE_LEFT
    assert captured_white_move_right.out == MOVE_WHITE_RIGHT
    assert captured_white_move_up.out == MOVE_WHITE_UP
    assert captured_white_move_down.out == MOVE_WHITE_DOWN

def test_placePwan(intialisedBoard):
    board = intialisedBoard
    board.pawn_positions["black"] = board.board[4][4].position
    board.pawn_positions["white"] = board.board[5][5].position
    board.placePawns()
    
    assert board.board[4][4].occupant == "black"
    assert board.board[5][5].occupant == "white"
    
    board.pawn_positions["black"] = board.board[2][4].position
    board.pawn_positions["white"] = board.board[3][4].position
    board.placePawns()
    
    assert board.board[2][4].occupant == "black"
    assert board.board[3][4].occupant == "white"

def test_removePawn(intialisedBoard):
    board = intialisedBoard
    #remove  initial pawns
    board.removePawns()
    assert board.board[0][4].occupant == None
    assert board.board[8][4].occupant == None
    
    board.pawn_positions["black"] = board.board[2][4].position
    board.pawn_positions["white"] = board.board[3][4].position
    
    board.removePawns()
    assert board.board[2][4].occupant == None
    assert board.board[3][4].occupant == None
    
    board.pawn_positions["black"] = board.board[5][4].position
    board.pawn_positions["white"] = board.board[3][4].position
    
    board.removePawns()
    assert board.board[5][4].occupant == None
    assert board.board[3][4].occupant == None
    
    board.pawn_positions["black"] = board.board[2][4].position
    board.pawn_positions["white"] = board.board[7][4].position
    
    board.removePawns()
    assert board.board[2][4].occupant == None
    assert board.board[7][4].occupant == None
    

def test_findWalledCells():
    random.seed(1716)
    pass

def test_copy(intialisedBoard):
    board = intialisedBoard
    board_copy = board.copy()
    
    assert board.board == board_copy.board
    assert board is not board_copy
    assert board.board is not board_copy.board
    assert board.board[0][4] is not board_copy.board[0][4]
    
    
    
    
        