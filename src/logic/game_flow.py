from utils import locationToCell
from game import Board, Pawn

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn(True, *board.pawn_positions['white'])
    black_pawn = Pawn(False, *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

def playGame(board, white_pawn, black_pawn):
    while True:
        # whites turn
        print(board.printBoard())
        print("White's turn\n")
        move = white_pawn.decideMoveHuman(board)
        makeMove(move, board, white_pawn.colour)
        white_pawn.position = board.pawn_positions['white']
        if(victory(white_pawn)):
            print("White wins!\n")
            break
        
        #blacks turn
        print(board.printBoard())
        print("Black's turn\n")
        move = black_pawn.decideMoveHuman(board)
        makeMove(move, board, black_pawn.colour)
        black_pawn.position = board.pawn_positions['black']
        if(victory(black_pawn)):
            print("Black wins!")
            break


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