from models.deep_q_learning import DQNAgent
from utils.utils import get_next_directory_number
from game import Board, Pawn
from models.train import step
from models.board_to_state import BoardToStateConverter
import numpy as np
import time
import pdb
import os

class Game:
    def __init__(self):
        print("\n\tWelcome to Quoridor!\n")
        self.board = Board()
        self.pawns = {
            'white': Pawn('white', *self.board.pawn_positions['white']),
            'black': Pawn('black', *self.board.pawn_positions['black'])
        }

    def play(self, colour, mode):
        board = self.board
        pawns = self.pawns
        white_agent_path = self.find_best_agent('src/trained_models/DQNagents', 'white')
        black_agent_path = self.find_best_agent('src/trained_models/DQNagents', 'black')    
        if not white_agent_path:
            print(f"No valid agent path found for {'white'}. Exiting function.")
            return
        if not black_agent_path:
            print(f"No valid agent path found for {'black'}. Exiting function.")
            return
        
        white_agent = DQNAgent((9, 9, 11), 330, 'white', pawns, epsilon=0, trained_model_path=white_agent_path)
        white_agent.load_model(white_agent.trained_model_path)
        white_agent.find_legal_moves(board.state)

        black_agent = DQNAgent((9, 9, 11), 330, 'black', pawns, epsilon=0, trained_model_path=black_agent_path)
        black_agent.load_model(black_agent.trained_model_path)
        black_agent.find_legal_moves(board.state)
        
        self.playGame(board, pawns['white'].copy(), pawns['black'].copy(), mode, white_agent, black_agent, colour)

    def playGame(self, board, white_pawn, black_pawn, mode, white_agent=None, black_agent=None, colour = 'white'):
        pawns = {
            'white': white_pawn,
            'black': black_pawn
        }
        
        if mode == 'pvp':
            self.player_vs_player(board, pawns)
        elif mode == 'eve':
            self.agent_vs_agent(board, white_agent, black_agent)
        elif mode == 'pve':
            agent = white_agent if colour == 'white' else black_agent
            self.player_vs_agent(board, pawns, agent)

    def player_vs_player(self, board, pawns):
        while True:
                #determine the pawn to move
                pawn = pawns['white'] if board.turn % 2 == 0 else pawns['black']

                #output whose turn it is
                print(f"Turn {board.turn}")
                print("White's turn" if board.turn % 2 == 0 else "Black's turn")
                print(pawn, "\n")

                #make a human move
                self.make_move_human(board, pawn, board.turn)

                #if the move lead to a victory exit
                if(self.victory(pawn)):
                    print("White Wins!\n" if board.turn % 2 == 0 else "Black Wins!\n")
                    break

    def player_vs_agent(self, board, pawns, agent):
        # Initialize a converter to transform the board state into a format the agent can understand
        board_state_converter = BoardToStateConverter()
        # Initialize a flag to check if the game is done
        done = False

        # Determine the human player's pawn based on the agent's colour
        human_pawn = pawns['black'] if agent.colour == 'white' else pawns['white']
        # pdb.set_trace()
        while True:
            # Determine whose turn it is and assign the appropriate pawn
            if(board.turn % 2 == 0):
                pawn = agent if agent.colour == 'white' else human_pawn
            else:
                pawn = agent if agent.colour == 'black' else human_pawn
                
            # Print the current state of the board and the turn information
            print(board.printBoard())
            print(f"Turn {board.turn}")
            print("White's turn" if board.turn % 2 == 0 else "Black's turn")
            
            # Check if it's the human player's turn
            if(hasattr(pawn, 'decideMoveHuman')):
                # If it is, let the human make a move
                self.make_move_human(board, pawn)
            else:
                # If it's the agent's turn, find the legal moves and make a move
                agent.find_legal_moves(board.state)
                board, done = self.make_move_agent(board.copy(), pawn, board_state_converter)

            # Check if the game is done after the agent's move
            if(done):
                # If the game is done, print the winning message and the final state of the board
                print(f"{agent.name} Wins! \nBetter Luck next time...")
                print(board)
                break
            
            # Check if the human player has won
            # pdb.set_trace()
            if(self.victory(human_pawn)):
                # If the human player has won, print the winning message and the final state of the board
                print(f"Congrats, You Won!")
                print(board)
                break

    def agent_vs_agent(self, board, white_agent, black_agent):
        
        #set the pawn positions for the agents
        white_agent.pawns['white'].position = board.pawn_positions['white']
        white_agent.pawns['black'].position = board.pawn_positions['black']
        black_agent.pawns['white'].position = board.pawn_positions['white']
        black_agent.pawns['black'].position = board.pawn_positions['black']
        
        board_state_converter = BoardToStateConverter()
        done = False
        while done:
            if board.turn % 2 == 0:
                board, done = self.make_move_agent(board.copy(), white_agent, board_state_converter)
            else:
                board, done = self.make_move_agent(board.copy(), black_agent, board_state_converter)
            if done:
                print("White Wins!\n" if board.turn % 2 == 0 else "Black Wins!\n")
                print(board)
            print(board)
            time.sleep(2)
        
    def make_move_human(self, board, pawn):
        #display the board
        print(board.printBoard())
        
        #while no valid move has been provided
        while(True):
            try:
                #request a move
                move = pawn.decideMoveHuman(board)
                if move is not None:
                    break
            except Exception as e:
                print('An unexpected error occurred. Please try entering your move again.\n')
                print('printing backtrace: ', e)

        #make the move (increments the turn number and updates the board state)
        board.makeMove(move, board, pawn.colour)

        #update the pawn's number of walls
        if(move.action == 'place'):
            pawn.walls -= 1

        #update the pawn's position
        pawn.position = board.pawn_positions[pawn.colour]

    def make_move_agent(self, board, agent, board_state_converter):
        state = board_state_converter.boardToState(board, agent.pawns)
        agent.find_legal_moves(board.state)
        state = np.reshape(state, [1, *agent.state_shape])
        action = agent.act(state)
        next_state, reward, board, done = step(board.copy(), action, agent, board_state_converter)
        next_state = np.reshape(next_state, [1, *agent.state_shape])
        agent.remember(state, action, reward,  next_state, done)
        state = next_state
        if (90000 <= action <= 98811):
            agent.pawns[agent.colour].walls -= 1 
        
        return board.copy(), done

    def replayGame(self, agent):
        agent.batach_size = len(agent.memory)
        agent.replay(agent.batch_size)

    def non_human_victory(self, agent):
        goal_line = 0 if agent.colour == 'white' else 8
        if(agent.pawns[agent.colour].position[0] == goal_line):
            return True
        return False

    def victory(self, pawn):
        goal_line = 0 if pawn.colour == 'white' else 8
        if(pawn.position[0] == goal_line):
            return True
        return False  

    def find_best_agent(self, base_directory, agent_color):
        # This fetches the last completed generation number
        highest_gen = get_next_directory_number(base_directory, 'gen_') - 1
        for gen in range(highest_gen, -1, -1):  # Loop from highest_gen to 0
            gen_path = os.path.join(base_directory, f'gen_{gen}')
            results_path = os.path.join(gen_path, 'tournament_results.txt')
            
            if os.path.exists(results_path):
                # Process the file if it exists
                with open(results_path, 'r') as file:
                    lines = file.readlines()

                agent_scores = []
                parsing_data = False

                for line in lines:
                    line = line.strip()
                    if line.startswith('+---'):
                        parsing_data = not parsing_data  # Toggle on border lines
                        continue

                    if parsing_data and '|' in line:
                        parts = line.split('|')
                        if len(parts) > 2 and agent_color.capitalize() + '_Bot' in parts[1]:
                            agent_name = parts[1].strip()
                            try:
                                score = int(parts[2].strip())
                                # Parsing the agent number from the agent name
                                agent_number = agent_name.split('_')[-1]
                                agent_scores.append((agent_number, score))
                            except ValueError:
                                continue  # Skip malformed lines

                if agent_scores:
                    # Sort and pick the top agent by score
                    agent_scores.sort(key=lambda x: x[1], reverse=True)
                    best_agent_number = agent_scores[0][0]
                    best_agent_path = os.path.join(gen_path, f"{agent_color}_agents", f"agent_{best_agent_number}/")
                    return best_agent_path

        print(f"No results file found for any generation that includes a {agent_color} agent.")
        return None