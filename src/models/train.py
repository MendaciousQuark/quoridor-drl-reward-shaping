import numpy as np
from game import Move
from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, getCellDirection, moveNumberToLetter, opposingPawnAdjacent
from .board_to_state import boardToState
from .action_lookup import action_lookup
import time
import pdb

def trainDQN(agent, episodes, original_board, human=False, observe_from=None, observe_until=None, verbose=False):
        original_numbuer_of_walls_white = agent.pawns['white'].walls
        original_numbuer_of_walls_black = agent.pawns['black'].walls
        max_moves = 1000
        for e in range(episodes):
            start_time = time.time()  # Start tracking time

            state = reset(original_board, agent.pawns, original_numbuer_of_walls_white, original_numbuer_of_walls_black)
            agent.find_legal_moves(original_board.state)
            state = np.reshape(state, [1, *agent.state_shape])
            next_board = original_board.copy()
            while True:
                action = agent.act(state, verbose)
                next_state, reward, next_board, done = step(next_board, action, agent)
                next_state = np.reshape(next_state, [1, *agent.state_shape])
                agent.remember(state, action, reward, next_state, done)
                state = next_state

                agent.find_legal_moves(next_board.state)

                if(human):
                    if(observe_from is not None and observe_until is not None and observe_from <= e <= observe_until):
                        print(next_board)
                        print('reward:', reward)
                        print('turn:', next_board.turn)
                        time.sleep(1)
                    else:
                        print(next_board)
                        print('reward:', reward)
                        print('turn:', next_board.turn)

                # Calculate and print elapsed time
                end_time = time.time()  # Stop tracking time
                elapsed_time = end_time - start_time  # Calculate elapsed time
                print(f'\rElapsed time: {elapsed_time} seconds', end='', flush=True)

                if done or next_board.turn/2 > max_moves:
                    print(f'\rEpisode {e+1}/{episodes}, reward: {reward}')
                    break

            # Train with replay
            if len(agent.memory) > agent.batch_size:
                agent.replay(agent.batch_size)
                
def reset(board, pawns, original_numbuer_of_walls_white, original_numbuer_of_walls_black):
        pawns['white'].position = board.pawn_positions['white']
        pawns['black'].position = board.pawn_positions['black']
        pawns['white'].walls = original_numbuer_of_walls_white
        pawns['black'].walls = original_numbuer_of_walls_black
        return boardToState(board, pawns)
    
def step(next_board, action, agent):
    move = action_lookup[action]
    #if the action is mapped to a place move
    if((90000 <= action <= 98811)):
        #move is already a move object
        colour = move[0]
        start = move[1]
        orientation = move[2]
        move = Move(colour, start, None, 'place', None, None, orientation)
        agent.pawns[colour].walls -= 1
    #if the action is mapped to a movement
    else:
        #pdb.set_trace()
        colour = 'white' if next_board.turn % 2 == 0 else 'black'
        start = agent.pawns[colour].position
        #e1 e = j i = 1
        start_formatted = moveNumberToLetter(agent.pawns[colour].position[1]) + str(9 - agent.pawns[colour].position[0])
        adjacent_pawn = opposingPawnAdjacent(colour, next_board.board, next_board.board[start[0]][start[1]])
        jump_direction = None
        #if the adjacent pawn is not None and the action is a jump
        if(adjacent_pawn[0] and action in [4, 5, 6]):
            adjacent_pawn_direction = getCellDirection(start, adjacent_pawn[1].position)
        else:
            adjacent_pawn_direction = None
        #pdb.set_trace()
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
    #give a bonus for jumping over the opponent
    if(action in [4, 5, 6] and adjacent_pawn[0]):
        reward += 10
    passive_colour = 'black' if move.colour == 'white' else 'white'
    done = True if (victory(agent.pawns[move.colour]) or victory(agent.pawns[passive_colour])) else False
    next_board.updateState()
    return boardToState(next_board, agent.pawns), reward, next_board, done

def victory(pawn):
    if(pawn.colour == 'white'):
        return pawn.position[0] == 0
    else:
        return pawn.position[0] == 8