from src.game.board import Board, Cell
from tests.test_utils import *
import pytest, random

#Fixture to initialize the Board before each test automatically
@pytest.fixture(autouse=True)
def intialisedBoard():
    #create a new board and return it
    board = Board()
    return board

def test_initBoard(intialisedBoard):
    #assign the intialised board to a variable
    board = intialisedBoard
    #create a 2D list of cells to represent the initial state of the board
    start_test_board = [[Cell(i, j) for j in range(9)] for i in range(9)]
    #manually place the pawns on the board
    start_test_board[0][4].occupant = "black"
    start_test_board[8][4].occupant = "white"
    
    #assert that the board is as expected (equal)
    assert board.board == start_test_board
    
def test_printBoard(intialisedBoard, capsys):
    board = intialisedBoard
    #print the board
    print(board.printBoard())
    #capture the output
    captured = capsys.readouterr()
    #define the expected output
    expected_output = INIT_BOARD
    #assert that the output is as expected
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
    print(board.printBoard())
    #capture the output
    captured = capsys.readouterr()
    #define the expected output
    expected_output = PLACE_WALL_HORIZONTAL_THEN_VERTICAL
    
    assert captured.out == expected_output

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
    
    #place pawns and verify that they are placed
    board.pawn_positions["black"] = board.board[4][4].position
    board.pawn_positions["white"] = board.board[5][5].position
    board.placePawns()
    
    assert board.board[4][4].occupant == "black"
    assert board.board[5][5].occupant == "white"
    
    #repeat the process
    board.pawn_positions["black"] = board.board[2][4].position
    board.pawn_positions["white"] = board.board[3][4].position
    board.placePawns()
    
    assert board.board[2][4].occupant == "black"
    assert board.board[3][4].occupant == "white"

def test_removePawn(intialisedBoard):
    board = intialisedBoard
    #remove  pawns and verify that they are removed
    board.removePawns()
    assert board.board[0][4].occupant == None
    assert board.board[8][4].occupant == None
    
    #place new pawns
    board.pawn_positions["black"] = board.board[2][4].position
    board.pawn_positions["white"] = board.board[3][4].position
    
    #remove pawns and verify that they are removed
    board.removePawns()
    assert board.board[2][4].occupant == None
    assert board.board[3][4].occupant == None
    
    #repeat the process
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
    

from game.move import Move

def move_init_test():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert move.colour == True
    assert move.start == "e1"
    assert move.end == "e2"
    assert move.action == "move"
    assert move.direction == "up"
    assert move.jumpDirection == None
    assert move.orientation == None
    
def move_str_test():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert str(move) == f"Colour: {move.colour}\nAction: {move.action}\nStart: {move.start}\nEnd: {move.end}\nDirection: {move.direction}\nOrientation: {move.orientation}, jumpDirection: {move.jumpDirection}  "

def test_findWalledCells(intialisedBoard):
    # Initialize the board with the fixture
    board = intialisedBoard
    # Set a fixed seed for random operations to ensure test reproducibility
    random.seed(1716)

    # Define possible positions for placing vertical and horizontal walls
    possible_vertical_walls = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
    possible_horizontal_walls = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

    # Perform 100 iterations to test wall placement and cell detection under various configurations
    for i in range(100):
        # Create a copy of the board for each iteration to avoid modifying the original board
        temp_board = board.copy()
        
        # Randomly select 3 positions to place vertical walls
        vertical_walls = random.sample(possible_vertical_walls, 3)
        # Randomly select 3 positions to place horizontal walls
        horizontal_walls = random.sample(possible_horizontal_walls, 3)

        # Place the selected vertical walls on the temporary board
        for vertical_wall in vertical_walls:
            temp_board.placeWall("vertical", temp_board.board[vertical_wall[0]][vertical_wall[1]])
        
        # Place the selected horizontal walls on the temporary board
        for horizontal_wall in horizontal_walls:
            temp_board.placeWall("horizontal", temp_board.board[horizontal_wall[0]][horizontal_wall[1]])

        # Find all cells that are adjacent to walls using the board's method
        celled_walls_found = temp_board.findWalledCells()

        # Verify that each cell identified as being adjacent to a wall correctly has a wall
        for row in temp_board.board:
            for cell in row:
                if cell in celled_walls_found:
                    # Cells identified must have at least one wall
                    assert cell.has_wall_up or cell.has_wall_left
                else:
                    # Cells not identified should not have any adjacent walls
                    assert not cell.has_wall_up and not cell.has_wall_left

    

def test_copy(intialisedBoard):
    #creaste a deep copy of the board and verify that the board and its attributes are copied
    board = intialisedBoard
    board_copy = board.copy()
    
    assert board.board == board_copy.board
    #make sure the pointers are different
    assert board is not board_copy
    assert board.board is not board_copy.board
    assert board.board[0][4] is not board_copy.board[0][4]
    
    
    
    
        