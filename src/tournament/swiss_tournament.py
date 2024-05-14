from models.train import step
from game.board import Board
from models.board_to_state import BoardToStateConverter
from utils.utils import get_next_directory_number
from game.pawn import Pawn
import numpy as np
import os
import pdb
from tabulate import tabulate


class SwissTournament:
    def __init__(self, white_competitors, black_competitors, max_turns=200, base_path='src/trained_models/DQNagents'):
        self.white_competitors = white_competitors
        self.black_competitors = black_competitors
        self.base_path = base_path
        self.max_turns = max_turns
        self.scores = {agent: 0 for agent in self.black_competitors + self.white_competitors}
        self.rounds_played = {agent: 0 for agent in self.black_competitors + self.white_competitors}
        self.wins = {agent: 0 for agent in self.black_competitors + self.white_competitors}
        self.draws = {agent: 0 for agent in self.black_competitors + self.white_competitors}
        self.history = {agent: set() for agent in self.black_competitors + self.white_competitors}

    def compete(self, num_rounds, num_survivors_per_colour=1):
        for round_number in range(num_rounds):
            print(f"Starting Round {round_number + 1}")
            pairs = self.swiss_pairings(self.black_competitors, self.white_competitors, self.scores, self.history)
            
            results = []
            for i, pair in enumerate(pairs):
                print(f"Playing game between pair {i+1}")
                try:
                    result, turns_played = self.play_game(pair)
                except Exception as e:
                    print(f"An error occurred while playing game between pair {i+1}. Defaulting to draw.")
                    print(e)
                    result = 'draw'
                results.append(result)
            for index, result in enumerate(results):
                white, black = pairs[index]
                if not isinstance(result, str):
                    self.scores[result] += 1  # Increment score for the winning agent
                    self.wins[result] += 1
                else:
                    # Distribute 0.5 points each for a draw
                    self.scores[white] += 0.5
                    self.scores[black] += 0.5
                    self.draws[white] += 1
                    self.draws[black] += 1
                self.rounds_played[white] += turns_played
                self.rounds_played[black] += turns_played
        self.showResults()
        survivors = self.determine_survivors(num_survivors_per_colour)
        return survivors['white'], survivors['black'] # Return top 3 as survivors, adjust `n` as needed

    def determine_survivors(self, top_n_per_color):
        # Separate competitors by color
        white_scores = {agent: self.scores[agent] for agent in self.white_competitors}
        black_scores = {agent: self.scores[agent] for agent in self.black_competitors}

        # Sort competitors within each color by score and select the top N
        top_white = sorted(white_scores, key=white_scores.get, reverse=True)[:top_n_per_color]
        top_black = sorted(black_scores, key=black_scores.get, reverse=True)[:top_n_per_color]

        return {'white': top_white, 'black': top_black}

    def showResults(self):
        # Sort players by their scores in descending order
        sorted_scores = sorted(self.scores.items(), key=lambda item: (item[1], -self.rounds_played[item[0]]), reverse=True)
        
        # Prepare the leaderboard table
        leaderboard_table = []
        for agent, score in sorted_scores:
            total_rounds = self.rounds_played[agent]
            total_wins = self.wins[agent]
            total_draws = self.draws[agent]
            leaderboard_table.append([agent.name, score, total_rounds, total_wins, total_draws])
        
        # Print the leaderboard
        print(tabulate(leaderboard_table, headers=['Agent', 'Final Score', 'Rounds Played', 'Wins', 'Draws'], tablefmt='grid'))
        
        # Determine the generation directory to save the results
        next_gen = get_next_directory_number(self.base_path, 'gen_') - 1  # Fetching the latest generation folder
        results_file_path = os.path.join(self.base_path, f'gen_{next_gen}', 'tournament_results.txt')
        
        # Save the leaderboard to a file
        with open(results_file_path, 'w') as file:
            file.write(tabulate(leaderboard_table, headers=['Agent', 'Final Score', 'Rounds Played', 'Wins', 'Draws'], tablefmt='grid'))
        print(f"Results saved to {results_file_path}")


    def play_game(self, pair):
        board = Board()
        white_competitor, black_competitor = pair
        
        self.update_pawns(board, white_competitor, black_competitor)

        board.turn = 0
        board.updateState()
        board_state_converter = BoardToStateConverter()
        state = board_state_converter.boardToState(board, white_competitor.pawns)
        rounds_played = 0
        while board.turn < self.max_turns:
            rounds_played += 1
            self.update_pawns(board, white_competitor, black_competitor)
            agent = white_competitor if board.turn % 2 == 0 else black_competitor
            agent.find_legal_moves(board.state)
            state = np.reshape(state, [1, *agent.state_shape])
            action = agent.act(state)
            next_state, reward, board, done = step(board, action, agent, board_state_converter)
            next_state = np.reshape(next_state, [1, *agent.state_shape])
            agent.remember(state, action, reward,  next_state, done)
            state = next_state
            if (90000 <= action <= 98811):
                agent.pawns[agent.colour].walls -= 1      
            if done:
                return agent, rounds_played #return the winner
        return 'draw', rounds_played
        
    def update_pawns(self, board, white_competitor, black_competitor):
        white_competitor.pawns['white'] = Pawn('white', *board.pawn_positions['white'])
        white_competitor.pawns['black'] = Pawn('black', *board.pawn_positions['black'])
        black_competitor.pawns['white'] = Pawn('white', *board.pawn_positions['white'])
        black_competitor.pawns['black'] = Pawn('black', *board.pawn_positions['black'])

    def swiss_pairings(self, black_competitors, white_competitors, scores, history):
        # Sort both groups by scores in descending order and stabilize sorting by name
        sorted_blacks = sorted(black_competitors, key=lambda x: (-scores[x], x))
        sorted_whites = sorted(white_competitors, key=lambda x: (-scores[x], x))
        pairings = []
        used_blacks = set()
        used_whites = set()

        i = 0
        while i < len(sorted_blacks):
            black = sorted_blacks[i]
            if black in used_blacks:
                i += 1
                continue
            
            paired = False
            for white in sorted_whites:
                if white not in used_whites and white not in history[black]:
                    pairings.append((white, black))
                    history[black].add(white)
                    history[white].add(black)
                    used_blacks.add(black)
                    used_whites.add(white)
                    paired = True
                    break
            
            if not paired:
                print(f"No pairing found for {black.name}. This agent will wait for the next round.")
            
            i += 1

        return pairings
