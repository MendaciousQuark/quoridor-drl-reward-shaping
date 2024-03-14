
from utils import moveNumberToLetter
from models import DQNAgent, trainDQN, boardToState, step
from logic import playGame
from game import Board, Pawn

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn('white', *board.pawn_positions['white'])
    black_pawn = Pawn('black', *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def main():
    #playGame(*initGameObjects())
    board, white_pawn, black_pawn = initGameObjects()
    pawns = {
        'white': white_pawn,
        'black': black_pawn
    }
    
    agent = DQNAgent((9, 9, 6), 330, 'white', pawns)
    # finally:
    agent.find_legal_moves(board.state)
    # playGame(board, white_pawn, black_pawn, False, agent)
    for i in range(10000):
        print(f'Batch Episode {i+1}')
        try:
            agent = DQNAgent((9, 9, 6), 330, 'white', pawns)
            agent.load_model('src/trained_models')
        except:
            break
        if i > 1000:
            trainDQN(agent, 10, board, True)
        else:
            trainDQN(agent, 100, board)
        agent.save_model('src/trained_models')
    # print(board)
    # print(agent.act(boardToState(board, pawns)))
    # next_board, reward, _ = step(board, agent.act(boardToState(board, pawns)), agent)
    # print(next_board)
    # print('reward:', reward)

if __name__ == '__main__':
    main()
