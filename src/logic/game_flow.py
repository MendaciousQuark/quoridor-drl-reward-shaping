from utils import locationToCell

def makeMove(move, board, colour):
        if(move.action == "move" or move.action == "jump"):
            print(move)
            board.movePawn(colour, move.end)
        elif(move.action == "place"):
            board.placeWall(move.orientation, locationToCell(*move.start, board.board))