import numpy as np

def boardToState(board, pawns):
    """Converts the board and pawn positions to a state for the DQN."""
    state = np.zeros((9, 9, 6))
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
    return state