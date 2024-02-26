from logic import playGame, initGameObjects
from game import Board
import pdb

def main():
    #playGame(*initGameObjects())
    board = Board()
    # #no path
    # board.placeWall('horizontal', board.board[4][0])
    # board.placeWall('horizontal', board.board[4][2])
    # board.placeWall('horizontal', board.board[4][4])
    # board.placeWall('horizontal', board.board[4][6])
    # board.placeWall('horizontal', board.board[2][7])
    # board.placeWall('vertical', board.board[2][7])
    # board.placeWall('vertical', board.board[4][2])
    # board.placeWall('vertical', board.board[4][3])
    
    #yes path
    board.placeWall('horizontal', board.board[4][0])
    board.placeWall('horizontal', board.board[4][2])
    board.placeWall('horizontal', board.board[4][4])
    board.placeWall('horizontal', board.board[4][6])
    board.placeWall('horizontal', board.board[2][7])
    board.placeWall('vertical', board.board[0][7])
    board.placeWall('vertical', board.board[2][6])
    board.placeWall('vertical', board.board[4][8])
    
    
    print(board.printBoard())


if __name__ == '__main__':
    main()
