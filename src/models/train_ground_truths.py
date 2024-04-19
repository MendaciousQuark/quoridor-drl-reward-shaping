from utils.load_board import loadBoard
from .board_to_state import BoardToStateConverter
from .multi_step import multiAgentMultiStep
import pdb
import os
import re
import time
import numpy as np

def trainWithGroundTruths(directory_path, common_name_prefix, agents):
    # Compile regex for file matching
    file_pattern = re.compile(rf'^{common_name_prefix}(\d+)')
    # Lists to hold game data
    boards, pawn_dicts, game_infos = load_ground_truths(directory_path, file_pattern)

    # Prepare for batch processing
    board_state_converter = BoardToStateConverter()

    # Process each board
    print(f"Training with {len(boards)} ground truths...")
    for i, board in enumerate(boards):
        start_time = time.time()
        print(f'\n Processing ground truth {i+1}/{len(boards)}...')
        #determine active agents
        test_0 = time.time()
        active_colour = 'white' if board.turn % 2 == 0 else 'black'
        active_agents = [agent for agent in agents if agent.colour == active_colour]
        rewards = np.zeros(len(active_agents), dtype=np.float32)
        active_boards = [board.copy() for _ in range(len(active_agents))]
        end_test0 = time.time()
        print("Execution time test 0:", {test_0 - end_test0})
        test_1 = time.time()
        #update pawn positions
        active_agent_white_pawns = [pawn_dicts[i]['white'].copy() for agent in active_agents]
        active_agent_black_pawns = [pawn_dicts[i]['black'].copy() for agent in active_agents]
        end_test1 = time.time()
        print("Execution time test 1:", {test_1 - end_test1})
        test_2 = time.time()
        for j, agent in enumerate(active_agents):
            agent.find_legal_moves(active_boards[j].state)
        end_test2 = time.time()
        print("Execution time test 2:", {test_2 - end_test2})
        # Prepare the states
        states = [board_state_converter.boardToState(active_boards[j], agent.pawns) for j, agent in enumerate(active_agents)]
        states = [np.reshape(state, [1, *agent.state_shape]) for agent, state in zip(active_agents, states)]

        test_3 = time.time()

        state, _, boards, done, actions = multiAgentMultiStep(active_agents, active_boards, board_state_converter, depth=1)

        end_test3 = time.time()

        print("Execution time test 3:", {test_3 - end_test3})        
        #reset agent colours
        test_4 = time.time()
        for agent in active_agents:
            agent.colour = active_colour
        #determine rewards
        for j, agent in enumerate(active_agents):
            rewards[j] = 1000 if actions[j] == game_infos[j]['a'] else -1000

        #let agents memorise
        for state, action, reward, done in zip(states, actions, rewards, done):
            for agent in active_agents:
                agent.remember(state, action, reward, state, done)
        end_test4 = time.time()
        print("Execution time test 4:", {test_4 - end_test4})


        # Print elapsed time for this ground truth
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print(f'\n Elapsed time for ground truth {i+1}/{len(boards)}: {int(minutes)} minutes {int(seconds)} seconds')

    for agent in agents:
        agent.replay(agent.batch_size)

def load_ground_truths(directory_path, file_pattern):
    # Load all ground truth data
    boards, pawn_dicts, game_infos = [], [], []
    for filename in os.listdir(directory_path):
        match = file_pattern.match(filename)
        if match:
            board, white_pawn, black_pawn, info = loadBoard(f'{directory_path}/{filename}')
            boards.append(board)
            pawn_dicts.append({'white': white_pawn, 'black': black_pawn})
            game_infos.append(info)
    return boards, pawn_dicts, game_infos