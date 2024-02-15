from game import Board, Pawn
from logic import makeMove

def main():
    # Initialize a Board instance
    board = Board()

    # Place a wall or modify the board in some way to test the output
    board.placeWall('horizontal', start_cell=board.board[3][0])
    board.placeWall('horizontal', start_cell=board.board[3][2])
    board.placeWall('horizontal', start_cell=board.board[3][4])
    board.placeWall('horizontal', start_cell=board.board[3][6])
    board.placeWall('vertical', start_cell=board.board[1][7])
    #board.board[3][3].occupant = 'white'

    
    #board.printBoard()
    print("\n")
    #print(board.board)
    # Print the board
    
    print(board.printBoard())
    pawn = Pawn(True, *board.pawn_positions['white'])
    move = pawn.decideMoveHuman(board)
    makeMove(move, board, pawn.colour)
    print(board.printBoard())


if __name__ == '__main__':
    main()
