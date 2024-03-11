from utils import locationToCell
from game import Board, Pawn
from logic import validateMove

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn(True, *board.pawn_positions['white'])
    black_pawn = Pawn(False, *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def playGame(board, white_pawn, black_pawn, human=True):
    i = 0
    round = 0
    if human:
        while True:
            pawn = white_pawn if i % 2 == 0 else black_pawn
            round = round + 1 if i % 2 == 0 else round
            print(board.printBoard())
            print(f"Round {round}")
            print("White's turn" if i % 2 == 0 else "Black's turn")
            print(pawn, "\n")
            while(True):
                try:
                    move = pawn.decideMoveHuman(board)
                    if move is not None:
                        break
                except Exception as e:
                    print('An unexpected error occurred. Please try entering your move again.\n')
                    print('printing backtrace: ', e)
            makeMove(move, board, pawn.colour)
            pawn.position = board.pawn_positions['white' if i % 2 == 0 else 'black']
            if(victory(pawn)):
                print("White Wins!\n" if i % 2 == 0 else "Black Wins!\n")
                break
            if(move.action == 'place'):
                pawn.walls -= 1
            i += 1
    else:
        print("Not implemented yet.")

def victory(pawn):
    goal_line = 0 if pawn.colour else 8
    if(pawn.position[0] == goal_line):
        return True
    return False

def makeMove(move, board, colour):
        if(move.action == "move" or move.action == "jump"):
            board.movePawn(colour, move.end)
        elif(move.action == "place"):
            board.placeWall(move.orientation, locationToCell(*move.start, board.board))
            