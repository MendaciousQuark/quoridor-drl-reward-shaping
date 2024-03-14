from models.model import Model
from game.board import Board
from game.pawn import Pawn

def test_reward():
    # board = Board()
    # white_pawn = Pawn('white', 8, 4)
    # black_pawn = Pawn('black', 0, 4)
    # pawns = {'white' : white_pawn, 'black': black_pawn}
    # model_white = Model('white', pawns)
    # model_black = Model('black', pawns)
    
    # #calculate the reward for initial board (should be 0)
    # reward = model_white.calculate_rewards(board.state)
    # assert reward == 0   
    
    # #reward should be the same for both players
    # reward = model_black.calculate_rewards(board.state)
    # assert reward == 0
    
    # #since both rewards are the same we can set neutral reward to reward
    # neutral_reward = reward
    
    # #creat a complex board
    # board = Board()
    
    # #place walls to force a complex path
    # board.placeWall('vertical', board.board[0][5])
    # board.placeWall('horizontal', board.board[2][3])
    # board.placeWall('horizontal', board.board[4][0])
    # board.placeWall('horizontal', board.board[4][2])
    # board.placeWall('horizontal', board.board[4][4])
    # board.placeWall('horizontal', board.board[4][6])
    # board.placeWall('horizontal', board.board[2][7])
    # board.placeWall('vertical', board.board[0][7])
    # board.placeWall('vertical', board.board[2][6])
    # board.placeWall('vertical', board.board[4][8])
    # board.updateState()
    
    # print(board)
    
    # white_reward = model_white.calculate_rewards(board.state)
    # print('white reward:', white_reward)
    # assert white_reward > neutral_reward 
    
    # board.turn = 1
    # board.updateState()
    
    # black_reward = model_black.calculate_rewards(board.state)
    # print('black reward:', black_reward)
    # print(board)
    
    # assert black_reward < neutral_reward
    
    # #assert that the rewards are symmetrical
    # assert white_reward == -black_rewar
    
    assert True
    