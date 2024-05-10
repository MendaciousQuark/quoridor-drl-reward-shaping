from models.deep_q_learning import DQNAgent
from game.pawn import Pawn

def create_agents(agent_paths, colour):
    agents = []
    for path in agent_paths:
        name = path
        agent = DQNAgent((9, 9, 11), 330, colour, new_pawn_dict(), name=name, trained_model_path=path)
        agents.append(agent)
    return agents

def new_pawn_dict():
    return {
        'white': Pawn('white', *[8, 4]),
        'black': Pawn('black', *[0, 4])
    }