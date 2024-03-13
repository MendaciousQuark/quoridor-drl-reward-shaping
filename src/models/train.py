import numpy as np
from game import Move
from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, moveNumberToLetter
from .board_to_state import boardToState
from .action_lookup import action_lookup

def trainDQN(agent, episodes, original_board):
        for e in range(episodes):
            state = reset(original_board, agent.pawns)
            state = np.reshape(state, [1, *agent.state_shape])
            
            while True:
                action = agent.act(state)
                next_state, reward, done, _ = step(action, original_board.copy())
                next_state = np.reshape(next_state, [1, *agent.state_shape])
                agent.remember(state, action, reward, next_state, done)
                state = next_state
                
                if done:
                    break
                    
            # Train with replay
            if len(agent.memory) > agent.batch_size:
                agent.replay(agent.batch_size)
                
def reset(board, pawns):
        return boardToState(board, pawns)
    
def step(board, action, pawns):
    next_board = board.copy()
    move = action_lookup[action]
    #if the action is mapped to a place move
    if(isinstance(move, Move)):
        next_board.makeMove(move, next_board, move.colour)
    #if the action is mapped to a movement
    else:
        colour = 'white' if next_board.turn % 2 == 0 else 'black'
        start = pawns[colour].position
        #e1 e = j i = 1
        start_formatted = pawns[colour].position[1] + str(9 - pawns[colour].position[0])
        #def __init__(self, colour, start, end, action, direction, jumpDirection=None, orientation=None):
        if(move == 'up'):
            end = getDirectionIndex(start, UP)
            move = Move(colour, )
        elif(move == 'down'):
            pass
        elif(move == 'left'):
            pass
        elif(move == 'right'):
            pass
        elif(move == 'jumpo left'):
            pass
        elif(move == 'jump right'):
            pass
        elif(move == 'jump straight'):
            pass