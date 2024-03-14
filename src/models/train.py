import numpy as np
from game import Move
from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, getCellDirection, moveNumberToLetter, opposingPawnAdjacent
from .board_to_state import boardToState
from .action_lookup import action_lookup

def trainDQN(agent, episodes, original_board):
        for e in range(episodes):
            state = reset(original_board, agent.pawns)
            agent.find_legal_moves(original_board.state)
            state = np.reshape(state, [1, *agent.state_shape])
            
            while True:
                action = agent.act(state)
                next_state, reward, next_board, done= step(original_board.copy(), action, agent)
                next_state = np.reshape(next_state, [1, *agent.state_shape])
                agent.remember(state, action, reward, next_state, done)
                state = next_state
                
                agent.find_legal_moves(next_board.state)
                print(next_board)
                print('reward:', reward)
                if done:
                    break
                    
            # # Train with replay
            # if len(agent.memory) > agent.batch_size:
            #     agent.replay(agent.batch_size)
                
def reset(board, pawns):
        return boardToState(board, pawns)
    
def step(board, action, agent):
    next_board = board.copy()
    if(action == 4):
        print(board)
        for action in agent.action_state:
            if(action[0].action != 'place'):
                print('id:', action[1], 'action:', action[0].action)
    move = action_lookup[action]
    #if the action is mapped to a place move
    if(isinstance(move, Move)):
        #move is already a move object
        move = move
    #if the action is mapped to a movement
    else:
        colour = 'white' if next_board.turn % 2 == 0 else 'black'
        start = agent.pawns[colour].position
        #e1 e = j i = 1
        start_formatted = moveNumberToLetter(agent.pawns[colour].position[1]) + str(9 - agent.pawns[colour].position[0])
        adjacent_pawn = opposingPawnAdjacent(colour, next_board.board, next_board.board[start[0]][start[1]])
        jump_direction = None
        if(adjacent_pawn[0]):
            adjacent_pawn_direction = getCellDirection(start, adjacent_pawn[1].position)
        else:
            adjacent_pawn_direction = None
        #def __init__(self, colour, start, end, action, direction, jumpDirection=None, orientation=None):
        if(move == 'up'):
            end = getDirectionIndex(start, UP)
            direction = 'up'
            action = 'move'
        elif(move == 'down'):
            end = getDirectionIndex(start, DOWN)
            direction = 'down'
            action = 'move'
        elif(move == 'left'):
            end = getDirectionIndex(start, LEFT)
            direction = 'left'
            action = 'move'
        elif(move == 'right'):
            end = getDirectionIndex(start, RIGHT)
            direction = 'right'
            action = 'move'
        elif(move == 'jump left'):
            step_towards_opponet = getDirectionIndex(start, adjacent_pawn_direction)
            #left can me up and down too if the pawn is to the left or right of start
            if(adjacent_pawn_direction == LEFT):
                end = getDirectionIndex(step_towards_opponet, DOWN)
            elif(adjacent_pawn_direction == RIGHT):
                end = getDirectionIndex(step_towards_opponet, UP)
            #if the pawn is above or below the start then left is left
            else:
                end = getDirectionIndex(step_towards_opponet, LEFT)
            jump_direction = 'left'
        elif(move == 'jump right'):
            step_towards_opponet = getDirectionIndex(start, adjacent_pawn_direction)
            #right can me up and down too if the pawn is to the left or right of start
            if(adjacent_pawn_direction == LEFT):
                end = getDirectionIndex(step_towards_opponet, UP)
            elif(adjacent_pawn_direction == RIGHT):
                end = getDirectionIndex(step_towards_opponet, DOWN)
            #if the pawn is above or below the start then right is right
            else:
                end = getDirectionIndex(step_towards_opponet, RIGHT)
            jump_direction = 'right'
        elif(move == 'jump straight'):
            #if the jump is sttraight end is two steps in the direction of the adjacent pawn
            end = getDirectionIndex(adjacent_pawn[1].position, adjacent_pawn_direction)
        
        end_formatted = moveNumberToLetter(end[1]) + str(9 - end[0])
        if(action == 'move'):
            move = Move(colour, start_formatted, end_formatted, action, direction, None, None)
        else:
            move = Move(colour, start_formatted, end_formatted, action, None, jump_direction, None)
        
    #finally make the move
    next_board.makeMove(move, next_board, move.colour)
    
    #update the pawn position
    agent.pawns[move.colour].position = next_board.pawn_positions[move.colour]
    reward = agent.calculate_rewards(next_board.state)
    passive_colour = 'black' if move.colour == 'white' else 'white'
    done = True if (victory(agent.pawns[move.colour]) or victory(agent.pawns[passive_colour])) else False
    
    return boardToState(next_board, agent.pawns), reward, next_board, done

def victory(pawn):
    if(pawn.colour == 'white'):
        return pawn.position[0] == 8
    else:
        return pawn.position[0] == 0