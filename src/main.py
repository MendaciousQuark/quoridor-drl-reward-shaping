
from models import DQNAgent, Model
from models.train import trainDQN, trainWithGroundTruths
from logic import playGame
from game import Board, Pawn
from utils.save_board import saveBoard
from pathlib import Path
import os
import re
import random
import pdb

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn('white', *board.pawn_positions['white'])
    black_pawn = Pawn('black', *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def train(board, pawns, with_ground_truths = False, 
          use_pretrained = False, slow = False, verbose = False, 
          observe = True, observe_from = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91], 
          observe_until = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95], batch_episodes = 1000, batch_length = 15,
          number_of_agents = 10):

    pawns_copy = {
        'white': pawns['white'].copy(),
        'black': pawns['black'].copy()
    }
    
    n = number_of_agents
    agents = []
    
    #if n is not even add 1 until even
    while(n % 2 != 0):
        n += 1
    
    for i in range(n):
        if(i % 2 == 0):
            agent = DQNAgent((9, 9, 6), 330, 'white', pawns_copy)
        else:
            agent = DQNAgent((9, 9, 6), 330, 'black', pawns_copy)
        agent.trained_model_path = f'src/trained_models/DQNagents/agent_{i}/'
        agents.append(agent)
    
    #train the agents with groundtruth if requested via parameter
    if(with_ground_truths):
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
        for agent in agents:
            try:
                trainWithGroundTruths('src/models/ground_truths', 'ground_truth_', agents)
            except Exception as e:
                print(e)
            finally:
            #save the model after training
                agent.save_model(agent.trained_model_path)

    index = 0
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
                        agent = DQNAgent((9, 9, 6), 330, 'white', pawns_copy, 0.6)
                    else:
                        agent = DQNAgent((9, 9, 6), 330, 'black', pawns_copy, 0.6)
        except Exception as e:
            print(e)
            break
        observed = False
        try:
            if observe:
                if observe_from[index] <= i < observe_until[index]:
                    if(not slow):
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
                try:
                    agent.save_model(agent.trained_model_path)
                except Exception as e:
                    print(e)
                    pdb.set_trace()
            use_pretrained = True

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
    agent = DQNAgent((9, 9, 6), 330, colour, pawns, 0)
    agent.find_legal_moves(board.state)
    model_path = None
    if(colour == 'white'):
        model_path = 'src/trained_models/DQNagents/agent_0'
    else:
        model_path = 'src/trained_models/DQNagents/agent_1'
    agent.load_model(model_path)
    playGame(board, pawns['white'], pawns['black'], False, agent)
    
    #save the model after playing with it
    directory_path = Path(model_path)
    if not directory_path.exists():
        # If it doesn't exist, create it
        directory_path.mkdir(parents=True)
        print(f"Directory '{directory_path}' does not exist. Creating it.")
    else:
        # If it exists, you can proceed with your operations
        print(f"Directory '{directory_path}' already exists. Using it.")
    agent.save_model(model_path)

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


def get_next_file_number(directory_path, common_name_prefix):
    file_pattern = re.compile(rf'^{common_name_prefix}(\d+)')
    max_number = 0
    for filename in os.listdir(directory_path):
        match = file_pattern.match(filename)
        if match:
            current_number = int(match.group(1))
            if current_number > max_number:
                max_number = current_number
    return max_number + 1

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
    with_ground_truths = True
    if(training):
        train(board, pawns, with_ground_truths=with_ground_truths, use_pretrained=True, 
              observe=False, batch_episodes=1000, batch_length=15, number_of_agents=20)
    else:
        play(board, pawns, 'white', False,)
    # while True:
    #     creatGroundTruths()

if __name__ == '__main__':
    main()
