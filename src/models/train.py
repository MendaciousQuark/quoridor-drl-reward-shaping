import numpy as np
from game import Move
from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, getCellDirection, moveNumberToLetter, opposingPawnAdjacent
from .board_to_state import BoardToStateConverter
from .action_lookup import action_lookup
import time
import pdb

def trainDQN(agents, episodes, original_board, human=False, observe_from=None, observe_until=None, verbose=False):
        original_numbuer_of_walls_white = [agent.pawns['white'].walls for _, agent in enumerate(agents)]
        original_numbuer_of_walls_black = [agent.pawns['black'].walls for _, agent in enumerate(agents)]
        board_state_converter = BoardToStateConverter()
        states = [None for _ in range(len(agents))]
        next_boards = [original_board.copy() for _ in range(len(agents))]
        rewards = [0 for _ in range(len(agents))]
        done = [False for _ in range(len(agents))]
        max_moves = 1000
        for e in range(episodes):
            start_time = time.time()  # Start tracking time
            for i, agent in enumerate(agents):
                states[i] = reset(original_board, agent.pawns, original_numbuer_of_walls_white[i], original_numbuer_of_walls_black[i], board_state_converter)
                states[i] = np.reshape(states[i], [1, *agent.state_shape])
                agent.find_legal_moves(original_board.state)
                rewards[i] = 0
                next_boards[i] = original_board.copy()
                done[i] = False
            while True:
                #every two agents play on one board
                if(len(agents) > 1):
                    for i, agent in enumerate(agents):
                        turn_colour = 'white' if next_boards[i].turn % 2 == 0 else 'black'
                        if turn_colour == agent.colour == 'white':
                            action = agent.act(states[i], verbose)
                            next_state, rewards[i], next_boards[i], done[i] = step(next_boards[i], action, agent, board_state_converter, max_moves)
                            next_state = np.reshape(states[i], [1, *agent.state_shape])
                            states[i] = next_state
                            #update the board for black agent
                            states[i+1] = board_state_converter.copyState(states[i])
                            next_boards[i+1] = next_boards[i]
                            #find legal moves for the next agent
                            agent.find_legal_moves(next_boards[i].state)
                            agents[i+1].find_legal_moves(next_boards[i+1].state)
                            #remember the state
                            agent.remember(states[i], action, rewards[i], next_state, done[i])
                            done[i+1] = done[i]
                        elif turn_colour == agent.colour == 'black':
                            action = agent.act(states[i], verbose)
                            next_state, rewards[i], next_boards[i], done[i] = step(next_boards[i], action, agent, board_state_converter, max_moves)
                            next_state = np.reshape(states[i], [1, *agent.state_shape])
                            states[i] = next_state
                            #update the board for white agent
                            states[i-1] = board_state_converter.copyState(states[i])
                            next_boards[i-1] = next_boards[i]
                            #find legal moves for the agents
                            agent.find_legal_moves(next_boards[i].state)
                            agents[i-1].find_legal_moves(next_boards[i-1].state)
                            #remember the state
                            agent.remember(states[i], action, rewards[i], next_state, done[i])
                            done[i-1] = done[i]
                if(human):
                    if(observe_from is not None and observe_until is not None and observe_from <= e <= observe_until):
                        print(next_boards[0])
                        print('reward:', rewards[0])
                        print('turn:', next_boards[0].turn)
                        time.sleep(1)
                    else:
                        print(next_boards[0])
                        print('reward:', rewards[0])
                        print('turn:', next_boards[0].turn)

                # Calculate and print elapsed time
                # Calculate and print elapsed time
                end_time = time.time()  # Stop tracking time
                elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
                minutes, seconds = divmod(elapsed_time, 60)  # Convert elapsed time to minutes and seconds
                print(f'\rElapsed time: {int(minutes)} minutes {int(seconds)} seconds', end='', flush=True)

                all_done = True
                # Check if all agents are done
                for i, agent in enumerate(agents):
                    agent_done = done[i] or (next_boards[i].turn/2 > max_moves)
                    if agent_done:
                        #pdb.set_trace()
                        print(f'\nAgent {i+1} done, episode {e+1}/{episodes}, reward: {rewards[i]}')
                    all_done = agent_done and all_done
                if all_done:
                    print(f'\nEpisode {e+1}/{episodes}')
                    break

            # Train with replay
            print('Training with replay...')
            for i, agent in enumerate(agents):
                if len(agent.memory) > agent.batch_size:
                    print(f'\rAgent {i} replaying...', end='', flush=True)
                    agent.replay(agent.batch_size)
            print('\nDone training with replay')
                    
                
def reset(board, pawns, original_numbuer_of_walls_white, original_numbuer_of_walls_black, board_state_converter):
        pawns['white'].position = board.pawn_positions['white']
        pawns['black'].position = board.pawn_positions['black']
        pawns['white'].walls = original_numbuer_of_walls_white
        pawns['black'].walls = original_numbuer_of_walls_black
        return board_state_converter.boardToState(board, pawns)
    
def step(next_board, action, agent, board_state_converter, max_moves=100):
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
    done = True if (victory(agent.pawns[move.colour]) or victory(agent.pawns[passive_colour])) else False or (next_board.turn/2 > max_moves)
    next_board.updateState()
    return board_state_converter.boardToState(next_board, agent.pawns), reward, next_board, done

def victory(pawn):
    if(pawn.colour == 'white'):
        return pawn.position[0] == 0
    else:
        return pawn.position[0] == 8