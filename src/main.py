from game import Board, Pawn

def main():
    # Initialize a Board instance
    board = Board()

    
    # Place a wall or modify the board in some way to test the output
    board.placeWall('vertical', start_cell=board.board[1][2])
    board.placeWall('horizontal', start_cell=board.board[2][2])
    #board.board[1][1].occupant = 'white'

    
    #board.printBoard()
    print("\n")
    #print(board.board)
    # Print the board
    
    print(board.printBoard())
    
    pawn = Pawn(board.copy(), True, 0, 0)
    move = pawn.rquestMoveInput()
    print(str(move))


if __name__ == '__main__':
    main()
