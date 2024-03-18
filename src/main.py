
from utils import moveNumberToLetter
from models import DQNAgent, trainDQN
from logic import playGame
from game import Board, Pawn
from pathlib import Path

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn('white', *board.pawn_positions['white'])
    black_pawn = Pawn('black', *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def train(board, pawns):
    
    pawns_copy = {
        'white': pawns['white'].copy(),
        'black': pawns['black'].copy()
    }
    
    n = 2
    agents = []
    
    for i in range(n):
        if(i % 2 == 0):
            agent = DQNAgent((9, 9, 6), 330, 'white', pawns_copy)
        else:
            agent = DQNAgent((9, 9, 6), 330, 'black', pawns_copy)
        agent.trained_model_path = f'src/trained_models/DQNagents/agent_{i}/'
        agents.append(agent)
    # finally:
    agent.find_legal_moves(board.state)
    batch_episodes = 1000
    batch_length = 50
    observe_from =  [0, 11, 21, 31, 41, 51, 61, 71, 81, 91]
    observe_until = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
    slow = False
    use_pretrained = True
    index = 0
    for i in range(batch_episodes):
        print(f'Batch Episode {i+1}')
        pawns_copy = {
            'white': pawns['white'].copy(),
            'black': pawns['black'].copy()
        }
        try:
            if use_pretrained:
                for agent in agents:
                    agent.pawns = pawns_copy
                    agent.load_model(agent.trained_model_path)
                    agent.epsilon = 0.5
            else:
                agents = []
                agents.append(DQNAgent((9, 9, 6), 330, 'white', pawns_copy, 0.6))
                agents.append(DQNAgent((9, 9, 6), 330, 'black', pawns_copy, 0.6))
        except Exception as e:
            print(e)
            break
        observed = False
        if observe_from[index] <= i < observe_until[index]:
            if(not slow):
                trainDQN(agents, batch_length, board, True)
            else:
                trainDQN(agents, batch_length, board, True, observe_from, observe_until)
            observed = True
        elif i == observe_until[index]:
            index += 1
        if(not observed):
            trainDQN(agents, batch_length, board)
        for i, agent in enumerate(agents):
            agent.trained_model_path = f'src/trained_models/DQNagents/agent_{i}/'
            directory_path = Path(agent.trained_model_path)
            if not directory_path.exists():
                # If it doesn't exist, create it
                directory_path.mkdir(parents=True)
                print(f"Directory '{directory_path}' does not exist. Creating it.")
            else:
                # If it exists, you can proceed with your operations
                print(f"Directory '{directory_path}' already exists. Using it.")
            
            agent.save_model(agent.trained_model_path)
        use_pretrained = True
    
def play(board, pawns, human=False, agent=None):
    agent = DQNAgent((9, 9, 6), 330, 'white', pawns, 0)
    agent.find_legal_moves(board.state)
    agent.load_model('src/trained_models/DQNagents/agent_0')
    playGame(board, pawns['white'], pawns['black'], False, agent)
        
def main():
    board, white_pawn, black_pawn = initGameObjects()
    pawns = {
        'white': white_pawn,
        'black': black_pawn
    }
    
    train(board, pawns)
    #play(board, pawns, False)

if __name__ == '__main__':
    main()
