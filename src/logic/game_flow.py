from models.train import step
from models.board_to_state import BoardToStateConverter
import numpy as np

def playGame(board, white_pawn, black_pawn, human=True, agent=None):
    i = 0
    round = 0
    board_state_converter = BoardToStateConverter()
    pawns = {
        'white': white_pawn,
        'black': black_pawn
    }
    state = board_state_converter.boardToState(board, pawns)
    print(state.shape)
    if human:
        while True:
            board.turn = i
            pawn = white_pawn if i % 2 == 0 else black_pawn
            round = round + 1 if i % 2 == 0 else round
            print(board.printBoard())
            print(f"Round {round}")
            print("White's turn" if i % 2 == 0 else "Black's turn")
            print(pawn, "\n")
            while(True):
                try:
                    move = pawn.decideMoveHuman(board)
                    if move is not None:
                        break
                except Exception as e:
                    print('An unexpected error occurred. Please try entering your move again.\n')
                    print('printing backtrace: ', e)
            board.makeMove(move, board, pawn.colour)
            pawn.position = board.pawn_positions['white' if i % 2 == 0 else 'black']
            if(victory(pawn)):
                print("White Wins!\n" if i % 2 == 0 else "Black Wins!\n")
                break
            if(move.action == 'place'):
                pawn.walls -= 1
            i += 1
    else:
        while True:
            agent.find_legal_moves(board.state)
            pawn = agent if i % 2 == 0 else black_pawn
            round = round + 1 if i % 2 == 0 else round
            print(board.printBoard())
            print(f"Round {round}")
            print("White's turn" if i % 2 == 0 else "Black's turn")
            print(pawn, "\n")
            while(True):
                if(i % 2 == 0):
                    state = np.reshape(state, [1, *agent.state_shape])
                    action = pawn.act(state, board)
                    break
                else:
                    try:
                        move = pawn.decideMoveHuman(board)
                        if move is not None:
                            break
                    except Exception as e:
                        print('An unexpected error occurred. Please try entering your move again.\n')
                        print('printing backtrace: ', e)
            if(i % 2 == 0):
                state, _, board, _ = step(board, action, agent, board_state_converter)
                if (90000 <= action <= 98811):
                    white_pawn.walls -1
            else:
                board.makeMove(move, board, pawn.colour)
                pawn.position = board.pawn_positions['white' if i % 2 == 0 else 'black']
                if(move.action == 'place'):
                    pawn.walls -= 1
            if(i % 2 == 0):
                if(non_human_victory(pawn)):
                    print("White Wins!\n" if i % 2 == 0 else "Black Wins!\n")
                    break
            else:   
                if(victory(pawn)):
                    print("White Wins!\n" if i % 2 == 0 else "Black Wins!\n")
                    break
            i += 1

def non_human_victory(agent):
    goal_line = 0 if agent.colour == 'white' else 8
    if(agent.pawns[agent.colour].position[0] == goal_line):
        return True
    return False

def victory(pawn):
    goal_line = 0 if pawn.colour == 'white' else 8
    if(pawn.position[0] == goal_line):
        return True
    return False
            