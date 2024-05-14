
from models import DQNAgent, Model
from tournament.swiss_tournament import SwissTournament
from utils.utils import get_next_directory_number
from models.train import trainWithGroundTruths, step
from models.board_to_state import BoardToStateConverter
from utils.random_board import creatRandomBoard
import math
import os
import pdb

def evolveThroughTournament(agents, base_path='src/trained_models/DQNagents'):
    # Split agents into white and black agents
    white_agents = [agent for agent in agents if agent.colour == 'white']
    black_agents = [agent for agent in agents if agent.colour == 'black']
    
    number_of_children = 2
    num_survivors_per_colour = max(len(white_agents) // number_of_children, 1)
    rounds = math.ceil(math.log2(len(white_agents)))
    
    # Create a tournament
    tournament = SwissTournament(white_agents, black_agents, max_turns=100, base_path=base_path)
    
    # Compete in the tournament and get the top quarter of the agents
    white_survivors, black_survivors = tournament.compete(rounds, num_survivors_per_colour)
    
    # Calculate next generation directory
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
            
            # load the parent model onto the children
            white_child.load_model(white_survivor.trained_model_path)
            black_child.load_model(black_survivor.trained_model_path)

            # Mutate and save the white child
            # if it is the first hal of children keep the flags of the parent
            if j < (number_of_children // 2):
                white_child.flags = white_survivor.flags
                white_child.mutate_flags()
                
            white_child.store_flags()
            white_child.save_model(white_child.trained_model_path)
            children.append(white_child)
            
            # Mutate and save the black child
            # if it is the first hal of children keep the flags of the parent
            if j < (number_of_children // 2):
                black_child.flags = black_survivor.flags
                black_child.mutate_flags()

            black_child.store_flags()
            black_child.save_model(black_child.trained_model_path)
            children.append(black_child)
            
            #write the description of both children to a file
            write_description_to_file(white_child_path, white_child_description)
            write_description_to_file(black_child_path, black_child_description)
        
    # replace the agents with the children
    
    agents[:] = children

    # train the agents with groundtruths
    trainWithGroundTruths('src/models/ground_truths', 'ground_truth_', agents)
    return agents
 
def write_description_to_file(file_path, description):
    # Check if the file_path is not a file
    if not os.path.isfile(file_path):
        file_path = os.path.join(file_path, 'description.txt')
    
    # Write the description to the file
    with open(file_path, 'w') as file:
        file.write(description + "\n")
