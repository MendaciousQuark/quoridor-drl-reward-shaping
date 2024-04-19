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

def trainDQN(agents, episodes, original_board, human=False, observe_from=0, observe_until=1, verbose=False, slow=False):
    num_agents = len(agents)
    original_walls_white = np.array([agent.pawns['white'].walls for agent in agents])
    original_walls_black = np.array([agent.pawns['black'].walls for agent in agents])
    replay_queue = [[] for _ in range(num_agents)]
    board_state_converter = BoardToStateConverter()
    
    # Initialize states, next_boards, rewards, done using list comprehensions or numpy arrays
    states = [None] * num_agents
    next_boards = [original_board.copy() for _ in range(num_agents)]
    rewards = np.zeros(num_agents, dtype=np.float32)
    done = np.full(num_agents, False, dtype=bool)
    max_moves = 102

    for e in range(episodes):
        start_time = time.time()  # Start tracking time
        
        # Reset memories and states at the start of each episode
        for i, agent in enumerate(agents):
            agent.white_position_memory = []
            agent.black_position_memory = []
            agent.rewards_memory = []

        next_boards = [original_board.copy() for _ in range(num_agents)]
        states = batch_reset(next_boards, agents, original_walls_white, original_walls_black, board_state_converter)
        remembered = [False] * num_agents
        done = np.full(num_agents, False, dtype=bool)
        rewards = np.zeros(num_agents, dtype=np.float32)
        active_index = 0
        while not all(done):
            active_agents = [(agent, index) for index, agent in enumerate(agents) if agent.colour == ('white' if active_index % 2 == 0 else 'black') and not done[index]]
            if not active_agents:
                break
            print(f'\nActive agents: {len(active_agents)}', end='', flush=True)
            active_agent_list, active_indicies = zip(*active_agents) if active_agents else ([], [])
            active_states = [states[index] for index in active_indicies]
            active_boards = [next_boards[index] for index in active_indicies]
            for i, agent in enumerate(active_agent_list):
                try:
                    agent.find_legal_moves(active_boards[i].state)
                except Exception as e:
                    pdb.set_trace()
                    print(f'Error in find_legal_moves: {e}')

            actions = [agent.act(state, verbose) for agent, state in zip(active_agent_list, active_states)]
            new_states, new_rewards, new_boards, new_dones = multiAgentMultiStep(active_agent_list, active_boards, board_state_converter, max_moves=max_moves)

            for j, (agent_index, new_state, reward, new_board, is_done) in enumerate(zip(active_indicies, new_states, new_rewards, new_boards, new_dones)):
                opposite_index = agent_index + 1 if agent_index % 2 == 0 else agent_index - 1  # Assumes agents are paired consecutively
                states[agent_index] = np.reshape(new_state, [1, *agents[agent_index].state_shape])
                next_boards[agent_index] = new_board
                next_boards[opposite_index] = new_board  # Update the paired agent's board as well
                rewards[agent_index] = reward
                done[agent_index] = is_done
                done[opposite_index] = is_done  # Synchronize done status with paired agent
                if not remembered[agent_index]:
                    remembered[agent_index] = True
                    replay_queue[agent_index].append((states[agent_index], actions[j], rewards[agent_index], new_state, is_done))
                #reset agent colours to the right colour
                agents[agent_index].colour = 'white' if agent_index % 2 == 0 else 'black'
            active_index += 1  # Ensure this index is correctly initialized and incremented

            if human and observe_from <= e <= observe_until:
                #show the board between agents 0 an 1
                print(next_boards[0])
                if(slow):
                    time.sleep(1)

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print(f'\rEpisode {e+1}/{episodes} - Elapsed time: {int(minutes)} minutes {int(seconds)} seconds')

        print('Training with replay...')
        for index, agent in enumerate(agents):
            if len(replay_queue[index]) > agent.batch_size:
                agent.replay(replay_queue[index])
                replay_queue[index] = []  # Clear the queue after training
        print('Done training with replay.\n')

    print('Training complete.')

                    
def batch_reset(boards, agents, original_walls_white, original_walls_black, board_state_converter):
        states = []
        for board, agent, walls_white, walls_black in zip(boards, agents, original_walls_white, original_walls_black):
            agent.pawns['white'].position = board.pawn_positions['white']
            agent.pawns['black'].position = board.pawn_positions['black']
            agent.pawns['white'].walls = walls_white
            agent.pawns['black'].walls = walls_black
            state = board_state_converter.boardToState(board, agent.pawns)
            states.append(state)
        return [state.reshape(1, *agents[0].state_shape) for state in states]


def multiAgentMultiStep(agents, boards, board_state_converter, max_moves=100, depth=10, gamma=0.95):
    # Initialize rewards structure: Rows for agents, Columns for depth levels
    accumulated_rewards = np.zeros((len(agents), depth + 1))
    
    # Initial states and done flags
    states = [board_state_converter.boardToState(board, agent.pawns) for board, agent in zip(boards, agents)]
    states = [state.reshape(1, *agent.state_shape) for state, agent in zip(states, agents)]  # Proper reshaping
    dones = [False] * len(agents)

    # Containers for states, boards, and dones after the first move
    first_step_states = []
    first_step_boards = []
    first_step_dones = []

    # Process each depth level
    for d in range(depth):
        if all(dones):  # Early exit if all agents are done
            break
        
        # Get actions for only active agents
        active_indices = [index for index, done in enumerate(dones) if not done]
        active_agents = [agents[index] for index in active_indices]
        active_states = [states[index] for index in active_indices]
        active_boards = [boards[index] for index in active_indices]

        actions = [agent.act(state) for agent, state in zip(active_agents, active_states)]
        next_states, rewards, next_boards, new_dones = multiAgentStep(active_boards, actions, active_agents, board_state_converter, max_moves)
        
        # Save first step results separately
        if d == 0:
            first_step_boards = [board.copy() for board in next_boards]
            first_step_states = [board_state_converter.copyState(state) for state in next_states]
            first_step_dones = [True if done else False for done in new_dones]

        # Update global lists
        for index, (ns, nb, r, nd) in zip(active_indices, zip(next_states, next_boards, rewards, new_dones)):
            states[index] = ns.reshape(1, *agents[index].state_shape)
            boards[index] = nb
            if not dones[index]:  # Update rewards and dones if not done previously
                accumulated_rewards[index, d + 1] = accumulated_rewards[index, d] + r * (gamma ** d)
                dones[index] = nd or dones[index]

        # Flip colours and find legal moves for the next round
        for index in active_indices:
            agents[index].colour = 'white' if agents[index].colour == 'black' else 'black'
            agents[index].find_legal_moves(boards[index].state)
            #update the pawn positions for each agent
            agents[index].pawns['white'].position = boards[index].pawn_positions['white']
            agents[index].pawns['black'].position = boards[index].pawn_positions['black']

    # Final rewards considering depth and gamma
    final_rewards = accumulated_rewards[:, -1]  # Take the last column for final rewards
    return first_step_states, final_rewards, first_step_boards, first_step_dones

def multiAgentStep(next_boards, actions, agents, board_state_converter, max_moves=100):
    # Process actions into moves
    moves = vectorized_move_processing(actions, agents, next_boards)
    
    # Apply moves and get updated states, rewards, and game completion status
    next_boards, rewards, dones = apply_moves(agents, moves, next_boards, max_moves)
    
    # Convert the board states to a format suitable for neural network processing or further game logic
    states = [board_state_converter.boardToState(board, agent.pawns) for board, agent in zip(next_boards, agents)]
    for i, agent in enumerate(agents):
        next_board = next_boards[i]
        next_board.updateState()
        agent.pawns['white'].position = next_board.pawn_positions['white']
        agent.pawns['black'].position = next_board.pawn_positions['black']
    return states, rewards, next_boards, dones

def apply_moves(agents, moves, boards, max_moves):
    # Assume boards and moves are lists of board states and Move objects respectively
    for i, (agent, move, board) in enumerate(zip(agents, moves, boards)):
        # Apply each move to the corresponding board
        board.makeMove(move, board, move.colour)

        # Update pawn positions based on the new board state
        agent.pawns[move.colour].position = board.pawn_positions[move.colour]
        agent.pawns['white'].position = board.pawn_positions['white']
        agent.pawns['black'].position = board.pawn_positions['black']

        # Update the board state after all moves are applied
        board.updateState()

    # Calculate rewards and check game completion status in a batch/vectorized manner if possible
    rewards = np.array([agent.calculate_rewards(board.state) for agent, board in zip(agents, boards)])
    dones = np.array([check_victory(agent, board, max_moves) for agent, board in zip(agents, boards)])

    return boards, rewards, dones

def check_victory(agent, board, max_moves):
    colour = agent.colour
    passive_colour = 'black' if colour == 'white' else 'white'
    is_victory = victory(agent.pawns[colour]) or victory(agent.pawns[passive_colour])
    is_max_moves_exceeded = (board.turn / 2 > max_moves)
    return is_victory or is_max_moves_exceeded

def vectorized_move_processing(actions, agents, boards):
    actions = np.array(actions)
    place_mask = (actions >= 90000) & (actions <= 98811)  # Mask for place actions
    jump_mask = (actions >= 4) & (actions <= 6)          # Mask for jump actions
    normal_move_mask = (actions >= 0) & (actions <= 3)   # Mask for normal movement actions

    moves = np.empty(actions.shape[0], dtype=object)

    # Process place moves
    if np.any(place_mask):
        indices = np.where(place_mask)[0]
        for index in indices:
            action = actions[index]
            agent = agents[index]
            board = boards[index]
            move_details = action_lookup[action]
            colour, start, orientation = move_details[0], move_details[1], move_details[2]
            agent.pawns[colour].walls -= 1
            moves[index] = Move(colour, start, None, 'place', None, None, orientation)

    # Process normal moves
    if np.any(normal_move_mask):
        direction_map = {0: ('up', UP), 1: ('down', DOWN), 2: ('left', LEFT), 3: ('right', RIGHT)}
        indices = np.where(normal_move_mask)[0]
        for index in indices:
            agent = agents[index]
            board = boards[index]
            colour = agent.colour
            start = board.pawn_positions[colour]
            move_code = actions[index]
            direction = direction_map.get(move_code, ('up', UP))  # Default to 'up' if not found
            end = getDirectionIndex(start, direction[1])
            try:
                start_formatted = moveNumberToLetter(start[1]) + str(9 - start[0])
                end_formatted = moveNumberToLetter(end[1]) + str(9 - end[0])
                moves[index] = Move(colour, start_formatted, end_formatted, 'move', direction[0], None, None)
            except Exception as e:
                pdb.set_trace()
                print(f'Error in move processing: {e}')
    # Process jump moves
    if np.any(jump_mask):
        indices = np.where(jump_mask)[0]
        for index in indices:
            agent = agents[index]
            board = boards[index]
            start = board.pawn_positions[colour]
            jump_information = action_lookup[actions[index]]  # Decode jump information
            jump_direction, end = determine_jump_direction_and_end(jump_information, colour, start, board)
            try:
                start_formatted = moveNumberToLetter(start[1]) + str(9 - start[0])
                end_formatted = moveNumberToLetter(end[1]) + str(9 - end[0])
                moves[index] = Move(colour, start_formatted, end_formatted, 'jump', None, jump_direction, None)
            except Exception as e:
                pdb.set_trace()
                print(f'Error in jump move processing: {e}')

    return moves

def determine_jump_direction_and_end(jump_information, colour, start, board):
    adjacent_pawn = opposingPawnAdjacent(colour, board.board, board.board[start[0]][start[1]])
    adjacent_pawn_direction = getCellDirection(adjacent_pawn[1], board.board[start[0]][start[1]])
    if(jump_information == 'jump left'):
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
    elif(jump_information == 'jump right'):
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
    elif(jump_information == 'jump straight'):
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
    return jump_direction, end
    
def step(next_board, action, agent, board_state_converter, max_moves=100):
    
        
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
                states[j] = batch_reset(board, pawn_dicts[i], pawn_dicts[i]['white'].walls, pawn_dicts[i]['black'].walls, board_state_converter)
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

