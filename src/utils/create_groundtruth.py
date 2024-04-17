from utils.random_board import creatRandomBoard
from game.pawn import Pawn
from utils.save_board import saveBoard
from models.model import Model
from utils.utils import get_next_file_number
import random

def creatGroundTruth():
    action_ID  = None
    board, number_of_walls = creatRandomBoard()
    pawns = {
        'white': Pawn('white', *board.pawn_positions['white']),
        'black': Pawn('black', *board.pawn_positions['black'])
    }

    white_walls_used = random.randint(0, number_of_walls)
    black_walls_used = number_of_walls - white_walls_used
    pawns['white'].walls = max(10 - white_walls_used, 0)
    pawns['black'].walls = max(10 - black_walls_used, 0)

    colour = 'white' if board.turn % 2 == 0 else 'black'

    pawn = pawns[colour]
    
    model = Model(colour, pawns)

    #request a move (should be the best in the situation but dependant on user)
    print(board)
    print(f"White's turn" if colour == 'white' else "Black's turn")
    print(f"walls remaining = {pawns[colour].walls}")

    #save the move
    move = pawn.decideMoveHuman(board)
    
    #determine the action of the move and then get the id of the move based on that
    if(move.action == 'move' or move.action == 'jump'):
        action_ID = model.add_id_to_movement(move)[1]
    elif(move.action == 'place'):
        action_ID = model.add_id_to_place(move, *move.start)[1]
    else:
        raise ValueError("Invalid move action")
    
    #save the ground_truth
    ground_truth_number = get_next_file_number('src/models/ground_truths', 'ground_truth_')
    saveBoard(board, action_ID, pawns, f'src/models/ground_truths/ground_truth_{ground_truth_number}.txt')