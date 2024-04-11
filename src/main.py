
from models import DQNAgent, Model
from models.train import trainDQN, trainWithGroundTruths
from logic import playGame
from game import Board, Pawn
from utils.save_board import saveBoard
from utils.utils import get_next_file_number, get_next_directory_number
from pathlib import Path
from tournament.swiss_tournament import SwissTournament
import os
import random
import pdb
import math

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn('white', *board.pawn_positions['white'])
    black_pawn = Pawn('black', *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def train(board, pawns, with_ground_truths = False, 
          use_pretrained = False, slow = False, verbose = False, 
          observe = True, observe_from = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91], 
          observe_until = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95], batch_episodes = 1000, batch_length = 25,
          batches_per_generation = 2, number_of_agents = 10):

    pawns_copy = {
        'white': pawns['white'].copy(),
        'black': pawns['black'].copy()
    }
    
    n = number_of_agents
    agents = []
    
    #if n is not even add 1 until even
    while(n % 2 != 0):
        n += 1
    
    highest_gen = get_next_directory_number('src/trained_models/DQNagents', 'gen_') - 1 # -1 since we want the highest gen not gen + 1

    for i in range(n):
        if(i % 2 == 0):
            agent = DQNAgent((9, 9, 11), 330, 'white', pawns_copy, name=f"white_bot_{i}", trained_model_path=f'src/trained_models/DQNagents/gen_{highest_gen}/white_agents/agent_{i}/')
        else:
            agent = DQNAgent((9, 9, 11), 330, 'black', pawns_copy, name=f"black_bot_{i-1}", trained_model_path=f'src/trained_models/DQNagents/gen_{highest_gen}/black_agents/agent_{i}/')
        agents.append(agent)
    
    #if we are using pre-trained models, load them before training
    if use_pretrained:
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

    #train the agents with groundtruth if requested via parameter
    if(with_ground_truths):
        try:
            trainWithGroundTruths('src/models/ground_truths', 'ground_truth_', agents)
        except Exception as e:
            print(e)
        finally:
        #save the model after training
            agent.save_model(agent.trained_model_path)

    index = 0
    batches_since_evolution = 0
    #main training loop
    for i in range(batch_episodes):
        print(f'Batch Episode {i+1}')
        if(i > 0):
            board, pawns_copy = updateBoardAndPawns(board, pawns_copy)
            board.updateState()
        else:
            pawns_copy = {
                'white': pawns['white'].copy(),
                'black': pawns['black'].copy()
            }
        try:
            #every two episodes shuffle the opponents
            if(batches_since_evolution == batches_per_generation):
                agents = evolveThroughTournament(agents)
                batches_since_evolution = 0
            if(i % 2 == 0):
                agents = shuffle_opponents(agents) #opponents are each pair of agents (i.e. 0 and 1, 2 and 3, etc.)
            if use_pretrained:
                for agent in agents:
                    agent.pawns = pawns_copy
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
            else:
                agents = []
                for i in range(n):
                    if(i % 2 == 0):
                        agent = DQNAgent((9, 9, 11), 330, 'white', pawns_copy, 0.6, name=str(i), trained_model_path=f'src/trained_models/DQNagents/gen_{highest_gen}/white_agents/agent_{i}/')
                        agents.append(agent)
                    else:
                        agent = DQNAgent((9, 9, 11), 330, 'black', pawns_copy, 0.6, name=str(i), trained_model_path=f'src/trained_models/DQNagents/gen_{highest_gen}/black_agents/agent_{i}/')
                        agents.append(agent)
        except Exception as e:
            print(e)
            break
        observed = False
        try:
            if observe:
                if observe_from[index] <= i < observe_until[index]:
                    if(not slow):
                        pdb.set_trace()
                        trainDQN(agents, batch_length, board, observe)
                    else:
                        trainDQN(agents, batch_length, board, observe, observe_from[index], observe_until[index])
                    observed = True
                elif i == observe_until[index]:
                    index += 1
            if(not observed):
                trainDQN(agents, batch_length, board, verbose=verbose)
        except Exception as e:
            print(e)
        finally:
            for agent in agents:
                pdb.set_trace()
                try:
                    agent.save_model(agent.trained_model_path)
                    agent.store_flags(agent.trained_model_path)
                except Exception as e:
                    print(e)
            use_pretrained = True
            batches_since_evolution += 1

def evolveThroughTournament(agents):
    # Split agents into white and black agents
    white_agents = [agent for agent in agents if agent.colour == 'white']
    black_agents = [agent for agent in agents if agent.colour == 'black']
    
    number_of_children = 4
    num_survivors_per_colour = max(len(white_agents) // 4, 1)
    rounds = math.ceil(math.log2(len(white_agents)))
    
    # Create a tournament
    tournament = SwissTournament(white_agents, black_agents, max_turns=100)
    
    # Compete in the tournament and get the top quarter of the agents
    white_survivors, black_survivors = tournament.compete(rounds, num_survivors_per_colour)
    
    # Calculate next generation directory
    base_path = 'src/trained_models/DQNagents'
    next_gen = get_next_directory_number(base_path, 'gen_')
    next_gen_dir = f"gen_{next_gen}"
    
    children = []
    for i, (white_survivor, black_survivor) in enumerate(zip(white_survivors, black_survivors)):
        for j in range(number_of_children):
            agent_index = i * number_of_children + j
            white_child_path = os.path.join(base_path, next_gen_dir, 'white_agents', f'agent_{agent_index}')
            black_child_path = os.path.join(base_path, next_gen_dir, 'black_agents', f'agent_{agent_index}')
            
            white_child_description = f"Child {j}/{number_of_children} of parent {white_survivor.name} from generation {next_gen-1}. \nPart of generation {next_gen_dir}."
            black_child_description = f"Child {j}/{number_of_children} of parent {black_survivor.name} from generation {next_gen-1}. \nPart of generation {next_gen_dir}."

            white_child = DQNAgent((9, 9, 11), 330, 'white', white_survivor.pawns, 0.6, name=f'White_Bot_{agent_index}', description=white_child_description, trained_model_path=white_child_path)
            black_child = DQNAgent((9, 9, 11), 330, 'black', black_survivor.pawns, 0.6, name=f'Black_Bot_{agent_index}', description=black_child_description, trained_model_path=black_child_path)
            
            # Mutate and save the white child
            white_child.mutate_flags()
            white_child.store_flags()
            white_child.save_model()
            children.append(white_child)
            
            # Mutate and save the black child
            black_child.mutate_flags()
            black_child.store_flags()
            black_child.save_model()
            children.append(black_child)
    # replace the agents with the children
    agents[:] = children
    return agents
            

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

def play(board, pawns, colour, human=False, agent=None):
    highest_gen = get_next_directory_number('src/trained_models/DQNagents', 'gen_') - 1 # -1 since we want the highest gen not gen + 1
    if(colour == 'white'):
        agent = DQNAgent((9, 9, 11), 330, colour, pawns, epsilon=0, trained_model_path=f"src/trained_models/DQNagents/gen_{highest_gen}/white_agents/agent_0/")
    else:
        agent = DQNAgent((9, 9, 11), 330, colour, pawns, epsilon=0, trained_model_path=f"src/trained_models/DQNagents/gen_{highest_gen}/black_agents/agent_0/")
    agent.find_legal_moves(board.state)
    agent.load_model(agent.trained_model_path)
    playGame(board, pawns['white'], pawns['black'], False, agent)
    
    #save the model after playing with it
    directory_path = Path(agent.trained_model_path)
    if not directory_path.exists():
        # If it doesn't exist, create it
        directory_path.mkdir(parents=True)
        print(f"Directory '{directory_path}' does not exist. Creating it.")
    else:
        # If it exists, you can proceed with your operations
        print(f"Directory '{directory_path}' already exists. Using it.")
    agent.save_model(agent.trained_model_path)

def creatGroundTruths():
    action_ID  = None
    board, number_of_walls = creatRandomBoard()
    pawns = {
        'white': Pawn('white', *board.pawn_positions['white']),
        'black': Pawn('black', *board.pawn_positions['black'])
    }

    white_walls_used = random.randint(0, number_of_walls)
    black_walls_used = number_of_walls - white_walls_used
    pawns['white'].walls = max(10 - white_walls_used, 0)
    pawns['black'].walls = max(10 - black_walls_used, 0)

    colour = 'white' if board.turn % 2 == 0 else 'black'

    pawn = pawns[colour]
    
    model = Model(colour, pawns)

    #request a move (should be the best in the situation but dependant on user)
    print(board)
    print(f"White's turn" if colour == 'white' else "Black's turn")
    print(f"walls remaining = {pawns[colour].walls}")

    #save the move
    move = pawn.decideMoveHuman(board)
    
    #determine the action of the move and then get the id of the move based on that
    if(move.action == 'move' or move.action == 'jump'):
        action_ID = model.add_id_to_movement(move)[1]
    elif(move.action == 'place'):
        action_ID = model.add_id_to_place(move, *move.start)[1]
    else:
        raise ValueError("Invalid move action")
    
    #save the ground_truth
    ground_truth_number = get_next_file_number('src/models/ground_truths', 'ground_truth_')
    saveBoard(board, action_ID, pawns, f'src/models/ground_truths/ground_truth_{ground_truth_number}.txt')

def creatRandomBoard():
    #remove all pawns
    board = Board()
    board.removePawns()
    number_of_walls = random.randint(0, 10)
    for i in range(number_of_walls):
        while True:
            try:
                #choose a random wall type
                wall_type = random.choice(['horizontal', 'vertical'])
                #choose a random cell that is not at the edge of the board
                cell_location = random.choice([(random.randint(1, 7), random.randint(0, 8)), (random.randint(0, 8), random.randint(1, 7))])
                cell = board.board[cell_location[0]][cell_location[1]]
                board.placeWall(wall_type, cell)
                break
            except Exception as e:
                continue
    
    #place pawns randomly
    #white shouldn't be on row 0
    board.pawn_positions['white'] = [random.randint(1, 8), random.randint(0, 8)]
    #black shouldn't be on row 8
    board.pawn_positions['black'] = [random.randint(0, 7), random.randint(0, 8)]
    board.placePawns()
    #chose a random even or odd number betweeen 0 and 11
    board.turn = random.choice([0, 11])
    board.updateState()
    
    return board.copy(), number_of_walls

def shuffle_opponents(agents):
    white_agents = [agent for agent in agents if agent.colour == 'white']
    black_agents = [agent for agent in agents if agent.colour == 'black']
    
    random.shuffle(white_agents)
    random.shuffle(black_agents)
    
    paired_agents = []
    for white_agent, black_agent in zip(white_agents, black_agents):
        paired_agents.extend([white_agent, black_agent])
    
    return paired_agents

def main():
    board, white_pawn, black_pawn = initGameObjects()
    pawns = {
        'white': white_pawn,
        'black': black_pawn
    }
    
    training = True
    if(training):
        train(board, pawns, with_ground_truths=True, use_pretrained=True, 
              observe=False, batch_episodes=1000, batch_length=20, number_of_agents=50, batches_per_generation=3)
    else:
        play(board, pawns, 'black', False)
    # while True:
    #     creatGroundTruths()
if __name__ == '__main__':
    main()
