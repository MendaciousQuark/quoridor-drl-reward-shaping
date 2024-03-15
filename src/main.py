
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

def train(board, white_pawn, pawns):
    agent = DQNAgent((9, 9, 6), 330, 'white', pawns)
    agent = DQNAgent((9, 9, 6), 330, 'black', pawns)
    # finally:
    agent.find_legal_moves(board.state)
    # playGame(board, white_pawn, black_pawn, False, agent)
    batch_episodes = 1000
    batch_length = 10
    observe_from =  [0, 11, 21, 31, 41, 51, 61, 71, 81, 91]
    observe_until = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
    slow = False
    use_pretrained = False
    agents = [agent]
    for i in range(batch_episodes):
        print(f'Batch Episode {i+1}')
        try:
            if use_pretrained:
                for agent in agents:
                    agent.load_model(agent.trained_model_path)
            else:
                agents = []
                agents.append(DQNAgent((9, 9, 6), 330, 'white', pawns, 0.6))
                agents.append(DQNAgent((9, 9, 6), 330, 'black', pawns, 0.6))
        except:
            break
        observed = False
        for index in observe_from:
            if observe_from[index] <= i < observe_until[index]:
                if(not slow):
                    trainDQN(agents, batch_length, board, True)
                else:
                    trainDQN(agents, batch_length, board, True, observe_from, observe_until)
                observed = True
            break
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
        
def main():
    #playGame(*initGameObjects())
    board, white_pawn, black_pawn = initGameObjects()
    pawns = {
        'white': white_pawn,
        'black': black_pawn
    }
    
    train(board, white_pawn, pawns)
    # print(board)
    # print(agent.act(boardToState(board, pawns)))
    # next_board, reward, _ = step(board, agent.act(boardToState(board, pawns)), agent)
    # print(next_board)
    # print('reward:', reward)

if __name__ == '__main__':
    main()
