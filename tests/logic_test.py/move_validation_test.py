from logic.move_validation import *
from game.board import Board
from game.move import Move
from utils.directions import *

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
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][4])
    move = Move(True, 'e4', 'g4', 'jump', None, 'right', None)
    print(board)
    
    #jump should be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == True
    
    #test from black to white this time
    start_cell = board.board[4][5]
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][5])
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
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][5])
    move = Move(True, 'f5', 'd5', 'jump', None, 'left', None)
    
    #jump should be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == True
    
    #test from black to white this time
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][4])
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
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[4][5])
    move = Move(False, 'f5', 'd5', 'jump', None, 'left', None)
    
    #jump should not be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == False
    
    #test from white to black this time
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][4])
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
    adjacent_pawn = opposingPawnAdjacent(True, board.board, board.board[5][4])
    move = Move(False, 'e5', 'e3', 'jump', None, 'up', None)
    
    #jump should not be blocked
    assert straightJumpBlocked(start_cell, board, adjacent_pawn, move) == False
    
    #test from white to black this time
    start_cell = board.board[4][4]
    adjacent_pawn = opposingPawnAdjacent(False, board.board, board.board[4][4])
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
    adjacent_pawn_white_horizontal = opposingPawnAdjacent(False, horizontal_jump_board.board, horizontal_jump_board.board[4][4])
    jump_white_horizontal_right_and_down = Move(True, 'e4', 'f5', 'jump', None, 'down', None)
    jump_white_horizontal_right_and_up = Move(True, 'e4', 'f3', 'jump', None, 'up', None)
    
    # vertical jump white to black
    start_cell_white_vertical = vertical_jump_board.board[4][4]
    adjacent_pawn_white_vertical = opposingPawnAdjacent(False, vertical_jump_board.board, vertical_jump_board.board[4][4])
    jump_white_vertical_down_and_right = Move(True, 'e4', 'f5', 'jump', None, 'right', None)
    jump_white_vertical_down_and_left = Move(True, 'e4', 'd5', 'jump', None, 'left', None)
    
    # horizontal jump black to white
    start_cell_black_horizontal = horizontal_jump_board.board[4][5]
    adjacent_pawn_black_horizontal = opposingPawnAdjacent(True, horizontal_jump_board.board, horizontal_jump_board.board[4][5])
    jump_black_horizontal_left_and_down = Move(False, 'f5', 'e4', 'jump', None, 'down', None)
    jump_black_horizontal_left_and_up = Move(False, 'f5', 'e6', 'jump', None, 'up', None)
    
    # vertical jump black to white
    start_cell_black_vertical = vertical_jump_board.board[5][4]
    adjacent_pawn_black_vertical = opposingPawnAdjacent(True, vertical_jump_board.board, vertical_jump_board.board[5][4])
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
    
    
    