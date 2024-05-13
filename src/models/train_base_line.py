from models.train import trainDQN
from models.training_setup import init_agents, load_pretrained, pre_train, prepare_batch, train_batch
from game.pawn import Pawn
from game.board import Board
import pdb

def init_baseline_training(with_ground_truths = False, 
          use_pretrained = False, learn_movement = False, slow = False, verbose = False, 
          observe = False, observe_from = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91], 
          observe_until = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95], batch_episodes = 1000, batch_length = 25,
          batches_per_generation = 2, number_of_agents = 10):

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
    
    agents = init_agents(pawns_copy, agents, number_of_agents, base_path='src/trained_models/BaselineAgents')
    
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
    #main training loop
    for i in range(batch_episodes):
        print(f'Batch Episode {i+1}')
        board, pawns_copy = prepare_batch(pawns, board, i)
        try:
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