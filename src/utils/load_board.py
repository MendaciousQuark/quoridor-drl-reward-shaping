from game.board import Board
from game.pawn import Pawn
import ast

def loadBoard(file_path = 'src\models\ground_truth\ground_truth_0.txt'):
    '''
    now need to reverse the saving process
    so the first 9 rows are the board
    since wall up and wall left are stored as 0 can use as boolean
    pawn uses 0 1 2 for none white and black so use if statements to convert
    walls are walls for white and black
    turn is the turn number
    action ID is the action ID

    then need to create the objects from the information
    '''
    #parse information from file
    with open(file_path, 'r') as file:
            game_info = {}
            board = Board()  # Initialize a Board object
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Process board state from the first 9 lines
            for i, line in enumerate(lines[:9]):
                cells_in_line = line.rstrip().split(',')
                for j, cell in enumerate(cells_in_line):
                    if cell:  # Check if cell is not an empty string
                        wall_up = bool(int(cell[0]))
                        wall_left = bool(int(cell[1]))
                        board.board[i][j].setWalls(wall_up, wall_left)  # Update cell's walls
                        
            # Process additional game information
            for line in lines[9:]:  # Skip the first 9 lines which represent the board
                key_value = line.strip().split(' = ')
                if key_value[0]:  # Check if the line is not empty
                    value = ast.literal_eval(key_value[1]) if '[' in key_value[1] else int(key_value[1])
                    game_info[key_value[0]] = value
            
            # Initialize Pawn objects
            white_pawn = Pawn('white', *game_info['wp']) if 'wp' in game_info else None
            black_pawn = Pawn('black', *game_info['bp']) if 'bp' in game_info else None

            # Update the number of walls for each pawn
            if white_pawn:
                white_pawn.walls = game_info['ww']
            if black_pawn:
                black_pawn.walls = game_info['bw']
            
            #update the board with the corrrect pawn positions, and turn number
            board.removePawns()
            board.pawn_positions['white'] = game_info['wp'] if 'wp' in game_info else None
            board.pawn_positions['black'] = game_info['bp'] if 'bp' in game_info else None
            board.placePawns()
            board.turn = game_info['t'] if 't' in game_info else None
            board.updateState()

            return board, white_pawn, black_pawn, game_info