from utils import UP, DOWN, LEFT, RIGHT, getDirectionIndex, getCellDirection, moveNumberToLetter, opposingPawnAdjacent
from .action_lookup import action_lookup
from game import Move
import numpy as np
import pdb


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
    # pdb.set_trace()
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
            first_step_actions = [x for x in actions]

        # Update global lists
        for index, (ns, nb, r, nd) in zip(active_indices, zip(next_states, next_boards, rewards, new_dones)):
            states[index] = ns.reshape(1, *agents[index].state_shape)
            boards[index] = nb
            if not dones[index]:  # Update rewards and dones if not done previously
                accumulated_rewards[index, d + 1] = accumulated_rewards[index, d] + r * (gamma ** d)
                dones[index] = nd or dones[index]

        # Flip colours and find legal moves for the next round
        for index in active_indices:
            #update the pawn positions for each agent
            agents[index].pawns['white'].position = boards[index].pawn_positions['white']
            agents[index].pawns['black'].position = boards[index].pawn_positions['black']

            agents[index].colour = 'white' if agents[index].colour == 'black' else 'black'
            agents[index].find_legal_moves(boards[index].state)
            

    # Final rewards considering depth and gamma
    final_rewards = accumulated_rewards[:, -1]  # Take the last column for final rewards
    return first_step_states, final_rewards, first_step_boards, first_step_dones, first_step_actions

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

        #if a wall was placed
        if move.action == 'place':
            agent.pawns[move.colour].walls -= 1

        # Update the board state after all moves are applied
        board.updateState()

    # Calculate rewards and check game completion status in a batch/vectorized manner if possible
    rewards = np.array([agent.calculate_rewards(board.state) for agent, board in zip(agents, boards)])
    dones = np.array([check_victory(agent, board, max_moves) for agent, board in zip(agents, boards)])

    return boards, rewards, dones

def check_victory(agent, board, max_moves):
    colour = agent.colour
    agent.pawns['white'].position = board.pawn_positions['white']
    agent.pawns['black'].position = board.pawn_positions['black']
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
            colour = agent.colour
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

def victory(pawn):
    if(pawn.colour == 'white'):
        return pawn.position[0] == 0
    else:
        return pawn.position[0] == 8