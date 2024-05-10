from utils.utils import get_next_directory_number, delete_previous_generations
from models.deep_q_learning import DQNAgent
from models.train import trainWithGroundTruths, trainDQN
from tournament.tournament_evoloution import evolveThroughTournament
from utils.random_board import creatRandomBoard
from game.pawn import Pawn
from game.board import Board
import random
import pdb

def init_training(with_ground_truths = False, 
          use_pretrained = False, learn_movement = False, slow = False, verbose = False, 
          observe = False, observe_from = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91], 
          observe_until = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95], batch_episodes = 1000, batch_length = 25,
          batches_per_generation = 2, number_of_agents = 10, delete_after = 0):

    board = Board()

    pawns = {
        'white': Pawn('white', *board.pawn_positions['white']),
        'black': Pawn('black', *board.pawn_positions['black'])
    }

    pawns_copy = {
        'white': pawns['white'].copy(),
        'black': pawns['black'].copy()
    }

    number_of_agents
    agents = []
    
    agents = init_agents(pawns_copy, agents, number_of_agents)
    
    #if we are using pre-trained models, load them before training
    if use_pretrained:
        load_pretrained(agents)

    #train the agents with groundtruth if requested via parameter
    if(with_ground_truths):
        pre_train(agents)
    
    #learn only movement actions
    if(learn_movement):
        print(f'\rLearning movement actions\n', end='', flush=True)
        for agent in agents:
            agent.pawns['white'].walls = 0
            agent.pawns['black'].walls = 0
        trainDQN(agents, batch_length, Board())
        #reset the walls
        for agent in agents:
            agent.pawns['white'].walls = 10
            agent.pawns['black'].walls = 10

    index = 0
    batches_since_evolution = 0
    generations_since_deletion = 0
    #main training loop
    for i in range(batch_episodes):
        print(f'Batch Episode {i+1}')
        board, pawns_copy = prepare_batch(pawns, board, i)
        try:
            #every two episodes shuffle the opponents
            if(batches_since_evolution == batches_per_generation):
                agents = evolveThroughTournament(agents)
                batches_since_evolution = 0
                generations_since_deletion += 1
                if(delete_after > 0 and generations_since_deletion == delete_after):
                    delete_previous_generations('src/trained_models/DQNagents')
                    generations_since_deletion = 0
            if(i % 2 == 0):
                agents = shuffle_opponents(agents) #opponents are each pair of agents (i.e. 0 and 1, 2 and 3, etc.)
            index = train_batch(agents, observe, observe_from, observe_until, 
                                batch_length, board, verbose, slow, index, i)
        except Exception as e:
            print(e)
        finally:
            for agent in agents:
                try:
                    agent.save_model(agent.trained_model_path)
                    agent.store_flags(agent.trained_model_path)
                except Exception as e:  
                    print(e)
            use_pretrained = True
            batches_since_evolution += 1

def init_agents(pawns_copy, agents, number_of_agents, base_path='src/trained_models/DQNagents'):
    #if n is not even add 1 until even
    while(number_of_agents % 2 != 0):
        number_of_agents += 1
    
    highest_gen = get_next_directory_number(base_path, 'gen_') - 1 # -1 since we want the highest gen not gen + 1

    for i in range(number_of_agents):
        if(i % 2 == 0):
            agent = DQNAgent((9, 9, 11), 330, 'white', pawns_copy, name=f"white_bot_{i}", trained_model_path=f'{base_path}/gen_{highest_gen}/white_agents/agent_{i}/')
        else:
            agent = DQNAgent((9, 9, 11), 330, 'black', pawns_copy, name=f"black_bot_{i-1}", trained_model_path=f'{base_path}/gen_{highest_gen}/black_agents/agent_{i}/')
        agents.append(agent)
    return agents

def  train_batch(agents, observe, observe_from, observe_until, batch_length, board, verbose, slow, index, i):
    if observe:
    # Check if current iteration is within the observe window
        if observe_from[index] <= i < observe_until[index]:
            if not slow:
                trainDQN(agents, batch_length, board, observe)
            else:
                trainDQN(agents, batch_length, board, observe, observe_from[index], observe_until[index])
        elif i == observe_until[index]:
            index += 1
            # If the observation period just ended, and you still need to train (non-observed training)
            trainDQN(agents, batch_length, board, verbose=verbose)
        else:
            # If outside of any observation period
            trainDQN(agents, batch_length, board, verbose=verbose)
    else:
        # If not observing at all, proceed with regular training
        trainDQN(agents, batch_length, board, verbose=verbose)
    return index

def shuffle_opponents(agents):
    white_agents = [agent for agent in agents if agent.colour == 'white']
    black_agents = [agent for agent in agents if agent.colour == 'black']
    
    random.shuffle(white_agents)
    random.shuffle(black_agents)
    
    paired_agents = []
    for white_agent, black_agent in zip(white_agents, black_agents):
        paired_agents.extend([white_agent, black_agent])
    return paired_agents

def pre_train(agents):
        try:
            trainWithGroundTruths('src/models/ground_truths', 'ground_truth_', agents)
        except Exception as e:
            print(e)
        finally:
        #save the model after training
            for agent in agents:
                agent.save_model(agent.trained_model_path)

def load_pretrained(agents):
    for agent in agents:
        try:
            # Load the model if it exists
            agent.load_model(agent.trained_model_path)
        except:
            # If the model doesn't exist, create it
            agent.save_model(agent.trained_model_path)
            agent.load_model(agent.trained_model_path)
        finally:
            # set exploration rate to 0.5
            agent.epsilon = 0.5

def prepare_batch(pawns, board, episode):
    pawns_copy = {
        'white': pawns['white'].copy(),
        'black': pawns['black'].copy()
    }
    if(episode > 0):
        board, pawns_copy = updateBoardAndPawns(board, pawns_copy)
        board.updateState()
    else:
        board = Board()
    return board, pawns_copy

def updateBoardAndPawns(board, pawns):
    board, number_of_walls = creatRandomBoard()
    #creat a black pawn and a white pawn
    pawns['white'] = Pawn('white', *board.pawn_positions['white'])
    pawns['black'] = Pawn('black', *board.pawn_positions['black'])
    
    #randomly assign 'walls used' to the pawns
    white_walls_used = random.randint(0, number_of_walls)
    black_walls_used = number_of_walls - white_walls_used
    pawns['white'].walls = max(10 - white_walls_used, 0)
    pawns['black'].walls = max(10 - black_walls_used, 0)
    
    return board, pawns