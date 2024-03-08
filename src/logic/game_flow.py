from utils import locationToCell
from game import Board, Pawn
from logic import validateMove

def initGameObjects():
    print("\n\tWelcome to Quoridor!\n")
    board = Board()
    white_pawn = Pawn(True, *board.pawn_positions['white'])
    black_pawn = Pawn(False, *board.pawn_positions['black'])
    return board, white_pawn, black_pawn

'''
move: 
m u e1 e2
m d e9 e8
p h e7
place v e7
move up e2 e3
move down e8 e7
jump down e8 e2
jump e8 e2 down
jump e4 e2 down
move e8 d8 left
move left e8 d8
move left e3 d3
move down d8 d7
move up d3 d4
move down d7 d6
place h d4
move down d6 g5
move down d6 d5
jump d4 d6 up
'''

def playGame(board, white_pawn, black_pawn):
    i = 0
    round = 0
    
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
            