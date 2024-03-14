from game.board import Board
from game.pawn import Pawn
from logic.game_flow import *
def test_victory():
    #place pawns in a winning positions
    white_pawn = Pawn('white', 0, 0)
    black_pawn = Pawn('black', 8, 8)
    
    #check if the game is won
    assert victory(white_pawn) == True
    assert victory(black_pawn) == True
    
    #not in winning position
    white_pawn.position = [1, 1]
    black_pawn.position = [7, 7]
    
    #check if the game is won
    assert victory(white_pawn) == False
    assert victory(black_pawn) == False