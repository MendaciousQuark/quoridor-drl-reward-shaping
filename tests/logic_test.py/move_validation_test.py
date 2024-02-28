from logic.move_validation import *
from game.board import Board
from game.move import Move
from utils.directions import *
from errors.move_validation_error import MoveValidationError

import pytest

def test_validateMoveAction():
    #init a board
    board = Board()
    
    #create moves that would be valid
    valid_move_white_up = Move(True, 'e1', 'e2', 'move', 'up', None, None)
    valid_move_white_right = Move(True, 'e1', 'f1', 'move', 'right', None, None)
    valid_move_white_left = Move(True, 'e1', 'd1', 'move', 'left', None, None)
    valid_move_black_down = Move(False, 'e9', 'e8', 'move', 'down', None, None)
    valid_move_black_right = Move(False, 'e9', 'f9', 'move', 'right', None, None)
    valid_move_black_left = Move(False, 'e9', 'd9', 'move', 'left', None, None)
    
    #check if validateMoveAction works as expected
    assert validateMoveAction(valid_move_white_up, board)[0] == True
    assert validateMoveAction(valid_move_white_right, board)[0] == True
    assert validateMoveAction(valid_move_white_left, board)[0] == True
    assert validateMoveAction(valid_move_black_down, board)[0] == True
    assert validateMoveAction(valid_move_black_right, board)[0] == True
    assert validateMoveAction(valid_move_black_left, board)[0] == True

    #create moves that would be invalid
    #moving multiple spaces
    invalid_move_white_up_multiple = Move(True, 'e1', 'e3', 'move', 'up', None, None)
    invalid_move_white_right_multiple = Move(True, 'e1', 'g1', 'move', 'right', None, None)
    invalid_move_white_left_multiple = Move(True, 'e1', 'c1', 'move', 'left', None, None)
    invalid_move_black_down_multiple = Move(False, 'e9', 'e6', 'move', 'down', None, None)
    invalid_move_black_right_multiple = Move(False, 'e9', 'g9', 'move', 'right', None, None)
    invalid_move_black_left_multiple = Move(False, 'e9', 'c9', 'move', 'left', None, None)
    
    #check if validateMoveAction works as expected
    multiple_space_moves = [invalid_move_white_up_multiple, invalid_move_white_right_multiple, invalid_move_white_left_multiple, invalid_move_black_down_multiple, invalid_move_black_right_multiple, invalid_move_black_left_multiple]
    for move in multiple_space_moves:
        with pytest.raises(ValueError):
            validateMoveAction(move, board)
    
    #moving no spaces
    invalid_move_white_up_single = Move(True, 'e1', 'e1', 'move', 'up', None, None)
    invalid_move_white_right_single = Move(True, 'e1', 'e1', 'move', 'right', None, None)
    invalid_move_white_left_single = Move(True, 'e1', 'e1', 'move', 'left', None, None)
    invalid_move_black_down_single = Move(False, 'e9', 'e9', 'move', 'down', None, None)
    invalid_move_black_right_single = Move(False, 'e9', 'e9', 'move', 'right', None, None)
    invalid_move_black_left_single = Move(False, 'e9', 'e9', 'move', 'left', None, None)
    
    #check if validateMoveAction works as expected
    no_space_moves = [invalid_move_white_up_single, invalid_move_white_right_single, invalid_move_white_left_single, invalid_move_black_down_single, invalid_move_black_right_single, invalid_move_black_left_single]
    for move in no_space_moves:
        with pytest.raises(MoveValidationError):
            validateMoveAction(move, board)
    
    #move pawns to the edge of the board
    board.removePawns()
    board.pawn_positions['white'] = board.board[0][0].position
    board.pawn_positions['black'] = board.board[8][8].position
    board.placePawns()
    
    #place some walls in the center of the board
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('vertical', board.board[4][4])
    board.placeWall('vertical', board.board[4][6])
    
    #move pawns to the center of the board
    board.removePawns()
    board.pawn_positions['white'] = board.board[4][4].position
    board.pawn_positions['black'] = board.board[4][5].position
    board.placePawns()
    
    #create moves that try to cross walls
    invalid_move_white_up_wall = Move(True, 'e5', 'e6', 'move', 'up', None, None)
    invalid_move_white_left_wall = Move(True, 'e5', 'd5', 'move', 'left', None, None)
    invalid_move_black_up_wall = Move(False, 'f5', 'f6', 'move', 'up', None, None)
    invalid_move_black_right_wall = Move(False, 'f5', 'g5', 'move', 'right', None, None)
    
    #check if validateMoveAction works as expected
    wall_crossing_moves = [invalid_move_white_up_wall, invalid_move_white_left_wall, invalid_move_black_up_wall, invalid_move_black_right_wall]
    for move in wall_crossing_moves:
        assert validateMoveAction(move, board)[0] == False
    
    #move pawns away from the walls
    board.removePawns()
    board.pawn_positions['white'] = board.board[6][6].position
    board.pawn_positions['black'] = board.board[6][7].position
    board.placePawns()
    
    #moves that aren't moving pawns
    invalid_move_white_up_not_pawn = Move(True, 'a1', 'a2', 'move', 'up', None, None)
    invalid_move_black_down_not_pawn = Move(False, 'a8', 'a7', 'move', 'down', None, None)
    
    #check if validateMoveAction works as expected
    not_pawn_moves = [invalid_move_white_up_not_pawn, invalid_move_black_down_not_pawn]
    
    
    #moving one pawn into another
    invalid_move_collision_white = Move(True, 'g6', 'g7', 'move', 'right', None, None)
    invalid_move_collision_black = Move(False, 'g7', 'g6', 'move', 'left', None, None)
    collision_moves = [invalid_move_collision_white, invalid_move_collision_black]
    
    #moving pawns of wrong colour
    invalid_move_wrong_colour_white = Move(False, 'g6', 'g7', 'move', 'right', None, None)
    invalid_move_wrong_colour_black = Move(True, 'g7', 'g6', 'move', 'left', None, None)
    wrong_colour_moves = [invalid_move_wrong_colour_white, invalid_move_wrong_colour_black]
    #checking if validateMoveAction works as expected
    combined_invalid_moves = not_pawn_moves + collision_moves + wrong_colour_moves
    for move in combined_invalid_moves:
        with pytest.raises(MoveValidationError):
            validateMoveAction(move, board)
    
def test_validateJumpAction():
    #init a board
    board = Board()
    
    #place pawns  next to eachother in the center of the board
    board.removePawns()
    board.pawn_positions['white'] = board.board[4][4].position
    board.pawn_positions['black'] = board.board[4][5].position
    board.placePawns()
    
    #create moves that would be valid
    valid_jump_right_white = Move(True, 'e5', 'g5', 'jump', None, 'right', None)
    valid_jump_left_black = Move(False, 'f5', 'd5', 'jump', None, 'left', None)
    
    #check if validateJumpAction works as expected
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][4])
    print(board)
    assert validateJumpAction(valid_jump_right_white, board)[0] == True
    assert validateJumpAction(valid_jump_left_black, board)[0] == True
    
    #indicate the wrong direction
    invalid_jump_indicate_right_white = Move(True, 'e5', 'c5', 'jump', None, 'right', None)
    
    assert validateJumpAction(invalid_jump_indicate_right_white, board)[0] == False
    
    #create moves that would be invalid
    #jumping without a pawn to jump over
    invalid_jump_left_white = Move(True, 'e5', 'c5', 'jump', None, 'left', None)
    invalid_jump_right_black = Move(False, 'f5', 'h5', 'jump', None, 'right', None)
    
    #check if validateJumpAction works as expected
    assert validateJumpAction(invalid_jump_left_white, board)[0] == False
    assert validateJumpAction(invalid_jump_right_black, board)[0] == False
    
    #place some walls in the center of the board
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('vertical', board.board[4][4])
    board.placeWall('vertical', board.board[4][6])
    
    #jumping over a wall
    invalid_jumpe_left_white_wall = Move(True, 'e5', 'c5', 'jump', None, 'left', None)
    invalid_jump_right_black_wall = Move(False, 'f5', 'h5', 'jump', None, 'right', None)
    
    #check if validateJumpAction works as expected
    assert validateJumpAction(invalid_jumpe_left_white_wall, board)[0] == False
    assert validateJumpAction(invalid_jump_right_black_wall, board)[0] == False
    
    #try to jump from square with no pawn
    invalid_jump_white = Move(True, 'e2', 'c2', 'jump', None, 'left', None)
    invalid_jump_black = Move(False, 'f3', 'h3', 'jump', None, 'right', None)
    
    #check if validateJumpAction works as expected
    invalid_moves = [invalid_jump_white, invalid_jump_black]
    for move in invalid_moves:
        with pytest.raises(MoveValidationError):
            validateJumpAction(move, board)
    
def test_validatePlaceAction():
    #init a board
    board = Board()
    
    #valid wall placements
    valid_wall_horizontal = Move(True, 'e5', None, 'place', None, None, 'horizontal')
    valid_wall_vertical = Move(False, 'f5', None, 'place', None, None, 'vertical')
    
    #check if validateWallPlacement works as expected
    assert validatePlaceAction(valid_wall_horizontal, board)[0] == True
    assert validatePlaceAction(valid_wall_vertical, board)[0] == True
    
    #invalid wall placements
    #placing a wall on the edge of the board
    invalid_wall_horizontal_edge = Move(True, 'i1', None, 'place', None, None, 'horizontal')
    invalid_wall_vertical_edge = Move(False, 'i1', None, 'place', None, None, 'vertical')
    
    #check if validateWallPlacement works as expected
    assert validatePlaceAction(invalid_wall_horizontal_edge, board)[0] == False
    assert validatePlaceAction(invalid_wall_vertical_edge, board)[0] == False
    
    #use new board
    board = Board()
    #placing walls for a more complex environment
    #doing board.placeWall('vertical', board.board[2][7]) blocks all paths
    board.placeWall('horizontal', board.board[4][0])
    board.placeWall('horizontal', board.board[4][2])
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('horizontal', board.board[4][6])
    board.placeWall('horizontal', board.board[2][7])
    board.placeWall('vertical', board.board[4][2])
    board.placeWall('vertical', board.board[2][7])
    board.placeWall('vertical', board.board[4][3])

    #walls ontop of eachother
    invalid_wall_horizontal_overlap = Move(True, 'e5', None, 'place', None, None, 'horizontal')
    invalid_wall_vertical_overlap = Move(False, 'c5', None, 'place', None, None, 'vertical')
    
    #check if validateWallPlacement works as expected
    assert validatePlaceAction(invalid_wall_horizontal_overlap, board)[0] == False
    assert validatePlaceAction(invalid_wall_vertical_overlap, board)[0] == False
    
    #placing this vertical wall blocks all paths
    invalid_wall_vertical_block = Move(True, 'h7', None, 'place', None, None, 'vertical')
    
    #check if validateWallPlacement works as expected
    assert validatePlaceAction(invalid_wall_vertical_block, board)[0] == False
    
    #use new board
    board = Board()
    
    #placing walls for a more complex environment#
    #doing board.placeWall('horizontal', board.board[2][7]) blocks all paths
    board.placeWall('horizontal', board.board[4][0])
    board.placeWall('horizontal', board.board[4][2])
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('horizontal', board.board[4][6])
    
    board.placeWall('vertical', board.board[4][2])
    board.placeWall('vertical', board.board[2][7])
    board.placeWall('vertical', board.board[4][3])
    
    #placing this horizontal wall blocks all paths
    invalid_wall_horizontal_block = Move(False, 'h7', None, 'place', None, None, 'horizontal')
    
    #check if validateWallPlacement works as expected
    assert validatePlaceAction(invalid_wall_horizontal_block, board)[0] == False
    
def test_space_for_wall():
    #init a board
    board = Board()
    
    #check if there is a space for a wall in the center of the board (both orientations)
    start_cell = board.board[4][4]
    assert spaceForWall(start_cell, 'horizontal', board) == True
    assert spaceForWall(start_cell, 'vertical', board) == True
    
    #check if there is a space for a wall in the corner (top left) of the board (both orientations)
    start_cell = board.board[0][0]
    #both should be false since you can't place a wall on the edge of the board
    assert spaceForWall(start_cell, 'horizontal', board) == False
    assert spaceForWall(start_cell, 'vertical', board) == False
    
    #check if there is a space for a wall in the corner (bottom right) of the board (both orientations)
    start_cell = board.board[8][8]
    #both should be false since they goes off the board
    assert spaceForWall(start_cell, 'horizontal', board) == False
    assert spaceForWall(start_cell, 'vertical', board) == False
    
    #check if there is a space for a wall in the corner (bottom left) of the board (both orientations)
    start_cell = board.board[8][0]
    #horizontal should be true since walls are placed up from the start cell
    assert spaceForWall(start_cell, 'horizontal', board) == True
    #vertical should be false since you can't place a wall on the edge of the board
    assert spaceForWall(start_cell, 'vertical', board) == False
    
    #check if there is a space for a wall in the corner (top right) of the board (both orientations)
    start_cell = board.board[0][8]
    #horizontal should be false since you can't place a wall on the edge of the board
    assert spaceForWall(start_cell, 'horizontal', board) == False
    #vertical should be true since walls are placed left from the start cell
    assert spaceForWall(start_cell, 'vertical', board) == True
    
    #place a wall in the center of the board
    board.placeWall('horizontal', board.board[4][4])
    
    #check if there is a space for a wall in the center of the board (both orientations)
    start_cell = board.board[4][4]
    #starting at 4, 4 there is a wall to the right so there is no space for a horizontal wall
    assert spaceForWall(start_cell, 'horizontal', board) == False
    #no wall below so vertical should be true
    assert spaceForWall(start_cell, 'vertical', board) == True
    
    #place a vertical wall at (4, 4)
    board.placeWall('vertical', board.board[4][4])
    
    #check if there is a space for a wall in the center of the board (both orientations)
    start_cell = board.board[4][4]
    #both should be false since there are walls in both orientations
    assert spaceForWall(start_cell, 'horizontal', board) == False
    assert spaceForWall(start_cell, 'vertical', board) == False
    
    #place a vertical wall at (4, 5)
    board.placeWall('vertical', board.board[4][5])
    
    #check if thers is space at (4, 5) (both orientations)
    start_cell = board.board[4][5]  
    #both should be false since there are walls in both orientations
    assert spaceForWall(start_cell, 'horizontal', board) == False
    assert spaceForWall(start_cell, 'vertical', board) == False
    
    #place a vertical wall at (4, 6)
    board.placeWall('vertical', board.board[4][6])
    
    #check if thers is space at (4, 6) (both orientations)
    start_cell = board.board[4][6]
    #horizontal should be true since there is no wall to the right (and no more wall in starting space)
    assert spaceForWall(start_cell, 'horizontal', board) == True
    #vertical should be false since there is a vertical wall in the starting space
    assert spaceForWall(start_cell, 'vertical', board) == False
    
def test_directionBlocked():
    #init a board
    board = Board()
    
    #isolate center cell
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('vertical', board.board[4][4])
    board.placeWall('vertical', board.board[4][5])
    board.placeWall('horizontal', board.board[5][4])
    
    start_cell = board.board[4][4]
    for direction in [UP, DOWN, LEFT, RIGHT]:
        #all directions should be blocked
        assert directionBlocked(direction, start_cell, board) == True
        
    #use a new board
    board = Board()
    
    #check without walls
    start_cell = board.board[4][4]
    for direction in [UP, DOWN, LEFT, RIGHT]:
        #all directions should be open
        assert directionBlocked(direction, start_cell, board) == False

def test_straightJumpBlocked():
    #init a board
    board = Board()
    
    #isolate center cell
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('vertical', board.board[4][4])
    board.placeWall('vertical', board.board[4][5])
    board.placeWall('horizontal', board.board[5][4])
    
    board.removePawns()
    board.pawn_positions['white'] = board.board[4][4].position
    board.pawn_positions['black'] = board.board[4][5].position
    board.placePawns()
    
    #initialise a jump to the left (jump format: jump start end direction)
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][4])
    move = Move(True, 'e4', 'g4', 'jump', None, 'right', None)
    
    #jump should be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == True
    
    #test from black to white this time
    start_cell = board.board[4][5]
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][5])
    move = Move(False, 'f5', 'd5', 'jump', None, 'left', None)
    
    #jump should be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == True
    
    #reverse pawn positions
    board.removePawns()
    board.pawn_positions['white'] = board.board[4][5].position
    board.pawn_positions['black'] = board.board[4][4].position
    board.placePawns()
    
    #test again in reverse
    start_cell = board.board[4][5]
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][5])
    move = Move(True, 'f5', 'd5', 'jump', None, 'left', None)
    
    #jump should be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == True
    
    #test from black to white this time
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][4])
    move = Move(False, 'e4', 'g4', 'jump', None, 'right', None)
    
    #jump should be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == True
    
    #use a new board
    board = Board()
    
    #place pawns next to each other (horizontally)
    board.removePawns()
    board.pawn_positions['white'] = board.board[4][4].position
    board.pawn_positions['black'] = board.board[4][5].position
    board.placePawns()
    
    #initialise a jump to the left for black (jump format: jump start end direction)
    start_cell = board.board[4][5]
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][5])
    move = Move(False, 'f5', 'd5', 'jump', None, 'left', None)
    
    #jump should not be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == False
    
    #test from white to black this time
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][4])
    move = Move(True, 'e4', 'g4', 'jump', None, 'right', None)
    
    #jump should not be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == False
    
    #place pawns next to each other (vertically)
    board.removePawns()
    board.pawn_positions['white'] = board.board[4][4].position
    board.pawn_positions['black'] = board.board[5][4].position
    board.placePawns()
    
    #initialise a jump up for black (jump format: jump start end direction)
    start_cell = board.board[5][4]
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[5][4])
    move = Move(False, 'e5', 'e3', 'jump', None, 'up', None)
    
    #jump should not be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == False
    
    #test from white to black this time
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][4])
    move = Move(True, 'e4', 'e6', 'jump', None, 'down', None)
    
    #jump should not be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == False
    
def test_validAlternateJumpDirection():
    #init boards
    horizontal_jump_board = Board()
    vertical_jump_board = Board()
    
    #place walls to allow for diagonal jumps (horizontally)
    horizontal_jump_board.placeWall('vertical', horizontal_jump_board.board[4][4])
    horizontal_jump_board.placeWall('vertical', horizontal_jump_board.board[4][6])
    #place pawns for horizontal jump
    horizontal_jump_board.removePawns()
    horizontal_jump_board.pawn_positions['white'] = horizontal_jump_board.board[4][4].position
    horizontal_jump_board.pawn_positions['black'] = horizontal_jump_board.board[4][5].position
    horizontal_jump_board.placePawns()
    
    #place walls to allow for diagonal jumps (vertically)
    vertical_jump_board.placeWall('horizontal', vertical_jump_board.board[4][4])
    vertical_jump_board.placeWall('horizontal', vertical_jump_board.board[6][4])
    #place pawns for vertical jump
    vertical_jump_board.removePawns()
    vertical_jump_board.pawn_positions['white'] = vertical_jump_board.board[4][4].position
    vertical_jump_board.pawn_positions['black'] = vertical_jump_board.board[5][4].position
    vertical_jump_board.placePawns()
    
    #create jump moves (jump format: jump start end direction)
    
    # horizontal jump white to black
    start_cell_white_horizontal = horizontal_jump_board.board[4][4]
    adjacent_pawn_white_horizontal = opposingPawnAdjacent(True, horizontal_jump_board.board, horizontal_jump_board.board[4][4])
    jump_white_horizontal_right_and_down = Move(True, 'e4', 'f5', 'jump', None, 'down', None)
    jump_white_horizontal_right_and_up = Move(True, 'e4', 'f3', 'jump', None, 'up', None)
    
    # vertical jump white to black
    start_cell_white_vertical = vertical_jump_board.board[4][4]
    adjacent_pawn_white_vertical = opposingPawnAdjacent(True, vertical_jump_board.board, vertical_jump_board.board[4][4])
    jump_white_vertical_down_and_right = Move(True, 'e4', 'f5', 'jump', None, 'right', None)
    jump_white_vertical_down_and_left = Move(True, 'e4', 'd5', 'jump', None, 'left', None)
    
    # horizontal jump black to white
    start_cell_black_horizontal = horizontal_jump_board.board[4][5]
    adjacent_pawn_black_horizontal = opposingPawnAdjacent(False, horizontal_jump_board.board, horizontal_jump_board.board[4][5])
    jump_black_horizontal_left_and_down = Move(False, 'f5', 'e4', 'jump', None, 'down', None)
    jump_black_horizontal_left_and_up = Move(False, 'f5', 'e6', 'jump', None, 'up', None)
    
    # vertical jump black to white
    start_cell_black_vertical = vertical_jump_board.board[5][4]
    adjacent_pawn_black_vertical = opposingPawnAdjacent(False, vertical_jump_board.board, vertical_jump_board.board[5][4])
    jump_black_vertical_up_and_right = Move(False, 'e5', 'f4', 'jump', None, 'right', None)
    jump_black_vertical_up_and_left = Move(False, 'e5', 'd4', 'jump', None, 'left', None)
    
    #should all be valid
    assert validAlternateJumpDirection(start_cell_white_horizontal, horizontal_jump_board, adjacent_pawn_white_horizontal, jump_white_horizontal_right_and_down) == True
    assert validAlternateJumpDirection(start_cell_white_horizontal, horizontal_jump_board, adjacent_pawn_white_horizontal, jump_white_horizontal_right_and_up) == True
    assert validAlternateJumpDirection(start_cell_white_vertical, vertical_jump_board, adjacent_pawn_white_vertical, jump_white_vertical_down_and_right) == True
    assert validAlternateJumpDirection(start_cell_white_vertical, vertical_jump_board, adjacent_pawn_white_vertical, jump_white_vertical_down_and_left) == True
    assert validAlternateJumpDirection(start_cell_black_horizontal, horizontal_jump_board, adjacent_pawn_black_horizontal, jump_black_horizontal_left_and_down) == True
    assert validAlternateJumpDirection(start_cell_black_horizontal, horizontal_jump_board, adjacent_pawn_black_horizontal, jump_black_horizontal_left_and_up) == True
    assert validAlternateJumpDirection(start_cell_black_vertical, vertical_jump_board, adjacent_pawn_black_vertical, jump_black_vertical_up_and_right) == True
    assert validAlternateJumpDirection(start_cell_black_vertical, vertical_jump_board, adjacent_pawn_black_vertical, jump_black_vertical_up_and_left) == True
    
    
    