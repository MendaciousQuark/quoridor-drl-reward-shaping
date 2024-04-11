from logic.a_star import aStar
from logic.board_to_graph import boardToGraph
from utils.utils import opposingPawnAdjacent
import numpy as np


class BoardToStateConverter:
    def boardToState(self, board, pawns):
        """Converts the board and pawn positions to a state for the DQN."""
        state = np.zeros((9, 9, 11))
        # channel 1: white position
        state[pawns['white'].position[0], pawns['white'].position[1], 0] = 1
        # channel 2: black position
        state[pawns['black'].position[0], pawns['black'].position[1], 1] = 1
        # channel 3: horizontal walls
        for walled_cell in board.state['walled_cells']['horizontal']:
            state[walled_cell.position[0], walled_cell.position[1], 2] = 1
        # channel 4: vertical walls
        for walled_cell in board.state['walled_cells']['vertical']:
            state[walled_cell.position[0], walled_cell.position[1], 3] = 1
        # channel 5: white walls remaining
        state[:, :, 4] = pawns['white'].walls
        # channel 6: black walls remaining
        state[:, :, 5] = pawns['black'].walls

        state[:, :, 6] = board.turn

        #set white goal
        white_goal = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
        #set black goal
        black_goal = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

        #create seperate graphs for white and black as they change when used in aStar
        white_graph = boardToGraph(board.board)
        black_graph = boardToGraph(board.board)

        #calculate the distance from goal for white and black
        white_distance = len(aStar(white_graph, 'white', pawns['white'].position, white_goal))
        black_distance = len(aStar(black_graph, 'black', pawns['black'].position, black_goal))
        distance_difference = white_distance - black_distance
        
        state[:, :, 7] = white_distance
        state[:, :, 8] = black_distance
        state[:, :, 9] = distance_difference

        #check if the pawns are adjacent to each other
        if(opposingPawnAdjacent('white', board.board, board.board[pawns['white'].position[0]][pawns['white'].position[1]])[0]):
            state[:, :, 10] = 1
        elif(opposingPawnAdjacent('black', board.board, board.board[pawns['black'].position[0]][pawns['black'].position[1]])):
            state[:, :, 10] = 1
        else:
            state[:, :, 10] = 0
        
        #maybe add adjaent walls next...

        return state
    
    def copyState(self, state):
        """Returns a copy of the state."""
        return np.copy(state)