import numpy as np
from game import Move
from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, getCellDirection, moveNumberToLetter, opposingPawnAdjacent
from utils.load_board import loadBoard
from .board_to_state import BoardToStateConverter
from .action_lookup import action_lookup
from logic.board_to_graph import boardToGraph
from logic.a_star import aStar
import time
import os
import re
import pdb
import random

def trainDQN(agents, episodes, original_board, human=False, observe_from=None, observe_until=None, verbose=False):
        original_numbuer_of_walls_white = [agent.pawns['white'].walls for _, agent in enumerate(agents)]
        original_numbuer_of_walls_black = [agent.pawns['black'].walls for _, agent in enumerate(agents)]
        replay_queue = [[] for _ in range(len(agents))]
        board_state_converter = BoardToStateConverter()
        states = [None for _ in range(len(agents))]
        next_boards = [original_board.copy() for _ in range(len(agents))]
        rewards = [0 for _ in range(len(agents))]
        done = [False for _ in range(len(agents))]
        remembered = [False for _ in range(len(agents))]
        max_moves = 102
        for e in range(episodes):
            start_time = time.time()  # Start tracking time
            for i, agent in enumerate(agents):
                agent.white_position_memory = []
                agent.black_position_memory = []
                agent.rewards_memory = []
                states[i] = reset(original_board, agent.pawns, original_numbuer_of_walls_white[i], original_numbuer_of_walls_black[i], board_state_converter)
                states[i] = np.reshape(states[i], [1, *agent.state_shape])
                agent.find_legal_moves(original_board.state)
                rewards[i] = 0
                next_boards[i] = original_board.copy()
                done[i] = False
            while True:
                #print(f'\rEpisode {e+1}/{episodes}, turn {next_boards[0].turn}', end='', flush=True)
                #every two agents play on one board
                if(len(agents) > 1):
                    for i, agent in enumerate(agents):
                        #find legal moves:
                        agent.find_legal_moves(next_boards[i].state)

                        #ensure pawns for agent are the same as the pawns on the board
                        agent.pawns['white'].position = next_boards[i].pawn_positions['white']
                        agent.pawns['black'].position = next_boards[i].pawn_positions['black']

                        if not done[i]:
                            if agent.colour == 'white':
                                action = agent.act(states[i], verbose)
                                next_state, _, next_boards[i], done[i], rewards[i] = multiStep(agent, states[i], next_boards[i], board_state_converter, accumulated_reward=rewards[i], depth=10, gamma=0.95)
                                next_state = np.reshape(states[i], [1, *agent.state_shape])
                                states[i] = next_state
                                #agent colout might be changed in multiStep so force it to be white as it originally was
                                agent.colour = 'white'
                                #update the board for black agent
                                states[i+1] = board_state_converter.copyState(states[i])
                                next_boards[i+1] = next_boards[i]
                                done[i+1] = done[i]
                            elif agent.colour == 'black':
                                action = agent.act(states[i], verbose)
                                next_state, _, next_boards[i], done[i], rewards[i] = multiStep(agent, next_state, next_boards[i], board_state_converter, accumulated_reward=rewards[i], depth=10, gamma=0.95)
                                next_state = np.reshape(next_state, [1, *agent.state_shape])
                                states[i] = next_state
                                #agent colout might be changed in multiStep so force it to be black as it originally was
                                agent.colour = 'black'
                                #update the board for white agent
                                states[i-1] = board_state_converter.copyState(states[i])
                                next_boards[i-1] = next_boards[i]
                                done[i-1] = done[i]
                            #remember the state
                            replay_queue[i].append((states[i], action, rewards[i], next_state, done[i]))
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

                if agentsDone(agents, next_boards, done, rewards, replay_queue, remembered, max_moves, e, episodes):
                    print(f'\n Time taken for episode {e+1}/{episodes}: {int(minutes)} minutes {int(seconds)} seconds')
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

def multiStep(agent, next_state, board, board_state_converter, accumulated_reward=0, depth=10, gamma=0.95):
    if depth == 0 or victory(agent.pawns['white']) or victory(agent.pawns['black']):
        # Base case: simply return the current state and the total accumulated reward
        return next_state, 0, board.copy(), True, accumulated_reward

    # Set agent color based on current turn
    agent.colour = 'white' if board.turn % 2 == 0 else 'black'
    
    # Agent finds legal moves and selects an action
    agent.find_legal_moves(board.state)
    action = agent.act(next_state)
    
    # Perform the action to get the new state and rewards
    next_state, immediate_reward, next_board, done = step(board.copy(), action, agent, board_state_converter)
    next_state = np.reshape(next_state, [1, *agent.state_shape])

    if done or victory(agent.pawns['white']) or victory(agent.pawns['black']):
        # If game ends, return the state and total rewards including the immediate reward
        return next_state, immediate_reward, next_board, done, accumulated_reward + immediate_reward

    # Update accumulated reward
    current_accumulated_reward = accumulated_reward + immediate_reward

    # Recursive call without prematurely scaling by gamma
    _, _, _, _, future_rewards = multiStep(agent, next_state, next_board, board_state_converter, 
                                           current_accumulated_reward, depth-1, gamma)

    # Calculate total reward using gamma only for future rewards
    total_reward = accumulated_reward + immediate_reward + gamma * future_rewards

    return next_state, immediate_reward, next_board, done, total_reward

    
def step(next_board, action, agent, board_state_converter, max_moves=100):
    move = action_lookup[action]
    #if the action is mapped to a place move
    if((90000 <= action <= 98811)):
        colour = move[0]
        start = move[1]
        orientation = move[2]
        move = Move(colour, start, None, 'place', None, None, orientation)
        agent.pawns[colour].walls -= 1
    #if the action is mapped to a movement
    else:
        #pdb.set_trace()
        colour = agent.colour
        start = agent.pawns[colour].position
        #e1 e = j i = 1
        start_formatted = moveNumberToLetter(agent.pawns[colour].position[1]) + str(9 - agent.pawns[colour].position[0])
        adjacent_pawn = opposingPawnAdjacent(colour, next_board.board, next_board.board[start[0]][start[1]])
        jump_direction = None
        #if the adjacent pawn is not None and the action is a jump
        if(adjacent_pawn[0] and action in [4, 5, 6]):
            #pdb.set_trace()
            adjacent_pawn_direction = getCellDirection(adjacent_pawn[1], next_board.board[start[0]][start[1]])
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
            if(adjacent_pawn_direction == UP):
                jump_direction = 'up'
            elif(adjacent_pawn_direction == DOWN):
                jump_direction = 'down'
            elif(adjacent_pawn_direction == LEFT):
                jump_direction = 'left'
            elif(adjacent_pawn_direction == RIGHT):
                jump_direction = 'right'
        try:        
            end_formatted = moveNumberToLetter(end[1]) + str(9 - end[0])
        except:
            pdb.set_trace()
        if(action == 'move'):
            try:
                move = Move(colour, start_formatted, end_formatted, action, direction, None, None)
            except:
                pdb.set_trace()
        else:
            action = 'jump'
            #pdb.set_trace()
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
    
    #update the board and the agent's pawn positions
    next_board.updateState()
    agent.pawns['white'].position = next_board.pawn_positions['white']
    agent.pawns['black'].position = next_board.pawn_positions['black']

    return board_state_converter.boardToState(next_board, agent.pawns), reward, next_board.copy(), done

def victory(pawn):
    if(pawn.colour == 'white'):
        return pawn.position[0] == 0
    else:
        return pawn.position[0] == 8

def agentsDone(agents, next_boards, done, rewards, replay_queue, remembered, max_moves, e, episodes):
    all_done = True
    # Check if all agents are done
    for i, agent in enumerate(agents):
        no_path = False
        if(aStar(boardToGraph(next_boards[i].board), 'white', agent.pawns['white'].position, [cell.position for cell in next_boards[i].board[0]]) == []):
            no_path = True
        if(aStar(boardToGraph(next_boards[i].board), 'black', agent.pawns['black'].position, [cell.position for cell in next_boards[i].board[0]]) == []):
            no_path = True
        agent_done = done[i] or (next_boards[i].turn/2 > max_moves) or no_path
        if agent_done:
            #pdb.set_trace()
            print(f'\nAgent {i+1} done, episode {e+1}/{episodes}, \nname: {agent.name} \ncolour: {agent.colour} \nreward: {rewards[i]}\n')
            if len(replay_queue[i]) < 101 and not no_path and done[i]: # Remember only if the game was not excessively long indicating many repeated moves
                if(not remembered[i]):
                    print(f'Agent {i+1} remembering episode {e+1}/{episodes}...')
                    for memory in replay_queue[i]:
                        agent.remember(*memory)
                    remembered[i] = True # Remember only once
                replay_queue[i] = []
        all_done = agent_done and all_done
    
    return all_done

def trainWithGroundTruths(directory_path, common_name_prefix, agents):
    '''
    for all ground truths:
        load it
        parse it
        put it in a list
    for all ground truths in the list:
        let the agent determine the bes move and then compare it to the ground truth
        if it is the same reward it
    '''
    boards = []
    pawn_dicts = []
    game_infos = []

    file_pattern = re.compile(rf'^{common_name_prefix}(\d+)')
    for filename in os.listdir(directory_path):
        match = file_pattern.match(filename)
        if match:
            current_board, current_white_pawn, current_black_pawn, current_info = loadBoard(f'{directory_path}/{filename}')
            boards.append(current_board)
            pawn_dicts.append({'white': current_white_pawn, 'black': current_black_pawn})
            game_infos.append(current_info)

    replay_queue = [[] for _ in range(len(agents))]
    board_state_converter = BoardToStateConverter()
    states = [None for _ in range(len(agents))]
    next_boards = [None for _ in range(len(agents))]
    rewards = [0 for _ in range(len(agents))]
    #the for loops should be the other way round for efficiency #FIXME
    print(f"Training with {len(boards)} ground truths...")
    for i, board in enumerate(boards):
        #start measuring time at the beginning of each ground truth
        start_time = time.time()
        for j, agent in enumerate(agents):
            print(f'\rAgent {j+1}/{len(agents)}', end='', flush=True)
            if(board.turn % 2 == 0 and agent.colour != 'white'):
                continue
            elif(board.turn % 2 == 1 and agent.colour != 'black'):
                continue
            else:
                #update the pawn positinos to represent the current board
                agent.pawns = pawn_dicts[i]
                agent.white_position_memory = []
                agent.black_position_memory = []
                agent.rewards_memory = []
                states[j] = reset(board, pawn_dicts[i], pawn_dicts[i]['white'].walls, pawn_dicts[i]['black'].walls, board_state_converter)
                states[j] = np.reshape(states[j], [1, *agent.state_shape])
                agent.find_legal_moves(board.state)
                rewards[j] = 0
                next_boards[j] = board.copy()
                
                #find the best move
                action = agent.act(states[j])
                next_state, rewards[j], next_boards[j], done = step(next_boards[j].copy(), action, agent, board_state_converter)
                next_state = np.reshape(next_state, [1, *agent.state_shape])

                #get the action id from the ground truth
                if(action == game_infos[i]['a']):
                    rewards[j] = 1000
                else:
                    rewards[j] = -1000

                #remember the state
                replay_queue[j].append((states[j], action, rewards[j], next_state, done))
        # Calculate and print elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        #print elapsed time and how many agents completed the ground truth
        print(f'\n\r Elapsed time for ground truth {i+1}/{len(boards)}: {int(minutes)} minutes {int(seconds)} seconds', end='', flush=True)
    
    # Train with replay
    print('Training with replay...')
    for i, agent in enumerate(agents):
        if len(agent.memory) > agent.batch_size:
            print(f'\rAgent {i} replaying...', end='', flush=True)
            agent.replay(agent.batch_size)

