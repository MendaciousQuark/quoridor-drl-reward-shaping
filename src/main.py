from logic import playGame
from game import Board, Pawn

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn(True, *board.pawn_positions['white'])
    black_pawn = Pawn(False, *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def main():
    playGame(*initGameObjects())

if __name__ == '__main__':
    main()
