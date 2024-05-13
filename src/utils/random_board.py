from game.board import Board
import random

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
    while True:
        black_pawn_row = random.randint(0, 7)
        black_pawn_col = random.randint(0, 8)
        if [black_pawn_row, black_pawn_col] != board.pawn_positions['white']:
            break
    board.pawn_positions['black'] = [black_pawn_row, black_pawn_col]
    board.pawn_positions['black'] = [random.randint(0, 7), random.randint(0, 8)]
    board.placePawns()
    #chose a random even or odd number betweeen 0 and 11
    board.turn = random.choice([0, 11])
    board.updateState()
    
    return board.copy(), number_of_walls