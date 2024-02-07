from game.board import Board

def main():
    # Initialize a Board instance
    board = Board()

    
    # Place a wall or modify the board in some way to test the output
    board.placeWall('horizontal', start_cell=board.board[0][0])
    board.board[1][1].occupant = 'white'

    # Print the board
    print(board.printBoard())  # Assuming printBoard returns a string representation of the board

if __name__ == '__main__':
    main()
