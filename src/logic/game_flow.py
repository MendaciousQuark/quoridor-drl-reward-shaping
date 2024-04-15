from models.train import step
from models.board_to_state import BoardToStateConverter
import numpy as np
import pdb

def playGame(board, white_pawn, black_pawn, human=True, agent=None):
    i = 0
    round = 0
    board_state_converter = BoardToStateConverter()
    pawns = {
        'white': white_pawn,
        'black': black_pawn
    }
        
        
    state = board_state_converter.boardToState(board, pawns)
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
        human_pawn = black_pawn if agent.colour == 'white' else white_pawn
        while True:
            agent.find_legal_moves(board.state)
            if(i % 2 == 0):
                pawn = agent if agent.colour == 'white' else human_pawn
            else:
                pawn = agent if agent.colour == 'black' else human_pawn
            round = round + 1 if i % 2 == 0 else round
            print(board.printBoard())
            print(f"Round {round}")
            print("White's turn" if i % 2 == 0 else "Black's turn")
            if(hasattr(pawn, 'decideMoveHuman')):
                print(pawn, "\n")
            else:
                print(pawn.name)
            while(True):
                if(hasattr(pawn, 'decideMoveHuman')):
                    try:
                        move = pawn.decideMoveHuman(board)
                        if move is not None:
                            break
                    except Exception as e:
                        print('An unexpected error occurred. Please try entering your move again.\n')
                        print('printing backtrace: ', e)
                else:
                    state = np.reshape(state, [1, *agent.state_shape])
                    action = pawn.act(state)
                    break
            if(hasattr(pawn, 'decideMoveHuman')):
                board.makeMove(move, board, pawn.colour)
                pawn.position = board.pawn_positions['white' if i % 2 == 0 else 'black']
                if(move.action == 'place'):
                    pawn.walls -= 1
                if(victory(pawn)):
                    print("White Wins!\n" if i % 2 == 0 else "Black Wins!\n")
                    print(board)
                    break
            else:
                next_state, reward, board, done = step(board, action, agent, board_state_converter)
                
                next_state = np.reshape(next_state, [1, *agent.state_shape])
                #states[i], action, rewards[i], next_state, done[i]
                pawn.remember(state, action, reward,  next_state, done)
                state = next_state
                if (90000 <= action <= 98811):
                    if(pawn.colour == 'white'):
                        white_pawn.walls -= 1
                    else:
                        black_pawn.walls -= 1
                if(non_human_victory(pawn)):
                    print("White Wins!\n" if i % 2 == 0 else "Black Wins!\n")
                    print(board)
                    break 
            i += 1
        # use played game as training
        replayGame(agent)

def replayGame(agent):
    agent.batach_size = len(agent.memory)
    agent.replay(agent.batch_size)
    
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
            