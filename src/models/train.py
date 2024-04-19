from .multi_step import multiAgentMultiStep
from .board_to_state import BoardToStateConverter
from logic.board_to_graph import boardToGraph
from logic.a_star import aStar
import numpy as np
import time
import pdb

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
            active_agent_list, active_indicies = zip(*active_agents) if active_agents else ([], [])
            active_states = [states[index] for index in active_indicies]
            active_boards = [next_boards[index].copy() for index in active_indicies]
            for i, agent in enumerate(active_agent_list):
                try:
                    agent.find_legal_moves(active_boards[i].state)
                except Exception as e:
                    pdb.set_trace()
                    print(f'Error in find_legal_moves: {e}')

            new_states, new_rewards, new_boards, new_dones, actions = multiAgentMultiStep(active_agent_list, active_boards, board_state_converter, max_moves=max_moves)

            for j, (agent_index, new_state, reward, new_board, is_done, action) in enumerate(zip(active_indicies, new_states, new_rewards, new_boards, new_dones, actions)):
                opposite_index = agent_index + 1 if agent_index % 2 == 0 else agent_index - 1  # Assumes agents are paired consecutively
                
                next_boards[agent_index] = new_board
                next_boards[opposite_index] = new_board  # Update the paired agent's board as well
                rewards[agent_index] = reward
                done[agent_index] = is_done
                done[opposite_index] = is_done  # Synchronize done status with paired agent
                # pdb.set_trace()
                if not remembered[agent_index]:
                    remembered[agent_index] = True
                    replay_queue[agent_index].append((states[agent_index], actions[j], rewards[agent_index], new_state, is_done))
                #reset agent colours to the right colour
                agents[agent_index].colour = 'white' if agent_index % 2 == 0 else 'black'

                #update states
                states[agent_index] = np.reshape(new_state, [1, *agents[agent_index].state_shape])
                states[opposite_index] = np.reshape(new_state, [1, *agents[opposite_index].state_shape])  # Update the paired agent's state as well
                agent.last_action = action
            active_index += 1  # Ensure this index is correctly initialized and incremented

            if human and observe_from <= e <= observe_until:
                #show the board between agents 0 an 1
                print(next_boards[0])
                print(done[0])
                if(slow):
                    time.sleep(1)

            end_time = time.time()
            print(f'\rEpisode {e+1}/{episodes} - Elapsed time: {int(end_time - start_time)} seconds', end='', flush=True)
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
