from utils.utils import *
from game.board import Board

import pytest

def test_validLocation():
    assert validLocation(0, 0) == True
    assert validLocation(0, 8) == True
    assert validLocation(8, 0) == True
    assert validLocation(8, 8) == True
    assert validLocation(4, 4) == True
    assert validLocation(-1, 0) == False
    assert validLocation(0, -1) == False
    assert validLocation(9, 0) == False
    assert validLocation(0, 9) == False
    assert validLocation(9, 9) == False
    
def test_joinWithNewlines():
    assert joinWithNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 3) == "abc\ndef\nghi"
    assert joinWithNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 1) == "a\nb\nc\nd\ne\nf\ng\nh\ni"
    assert joinWithNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 9) == "abcdefghi"
    assert joinWithNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 2) == "ab\ncd\nef\ngh\ni"
    assert joinWithNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 4) == "abcd\nefgh\ni"
    
def test_joinWithoutNewlines():
    assert joinWithoutNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 3) == "abcdefghi"
    assert joinWithoutNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 1) == "abcdefghi"
    assert joinWithoutNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 9) == "abcdefghi"
    assert joinWithoutNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 2) == "abcdefghi"
    assert joinWithoutNewlines(["a", "b", "c", "d", "e", "f", "g", "h", "i"], 4) == "abcdefghi"

def test_moveLetterToNumber():
    assert moveLetterToNumber("a") == 0
    assert moveLetterToNumber("b") == 1
    assert moveLetterToNumber("c") == 2
    assert moveLetterToNumber("d") == 3
    assert moveLetterToNumber("e") == 4
    assert moveLetterToNumber("f") == 5
    assert moveLetterToNumber("g") == 6
    assert moveLetterToNumber("h") == 7
    assert moveLetterToNumber("i") == 8
    
    with pytest.raises(ValueError):
        moveLetterToNumber("j")
    
    with pytest.raises(ValueError):
        moveLetterToNumber("2")
    
def test_moveNumberToLetter():
    assert moveNumberToLetter(0) == "a"
    assert moveNumberToLetter(1) == "b"
    assert moveNumberToLetter(2) == "c"
    assert moveNumberToLetter(3) == "d"
    assert moveNumberToLetter(4) == "e"
    assert moveNumberToLetter(5) == "f"
    assert moveNumberToLetter(6) == "g"
    assert moveNumberToLetter(7) == "h"
    assert moveNumberToLetter(8) == "i"
    
    with pytest.raises(ValueError):
        moveNumberToLetter(9)
    
    with pytest.raises(ValueError):
        moveNumberToLetter(-1)
    
    with pytest.raises(ValueError):
        moveNumberToLetter("a")
        
def test_findPawn():
    board = Board()
    pawn = findPawn(True, board.board)
    
    assert pawn.position == (8, 4)
    
    pawn = findPawn(False, board.board)
    
    assert pawn.position == (0, 4)
    
    board.board[0][4].occupant = None
    with pytest.raises(ValueError):
        pawn = findPawn(False, board.board)

def test_locationToCell():
    board = Board()
    cell = locationToCell(0, 0, board.board)
    
    assert cell == board.board[0][0]
    
    with pytest.raises(ValueError):
        cell = locationToCell(-1, 0, board.board)

def test_opposingPawnAdjacent():
    board = Board()
    #at board initialisation pawns are not adjacent
    white_pawn_adjacent = opposingPawnAdjacent('black', board.board, board.board[0][4])
    black_pawn_adjacent = opposingPawnAdjacent('white', board.board, board.board[8][4])
    
    #assert that the pawns are not adjacent
    assert white_pawn_adjacent[0] == False and white_pawn_adjacent[1] is None
    assert black_pawn_adjacent[0] == False and black_pawn_adjacent[1] is None

    board.removePawns()
    board.pawn_positions["black"] = board.board[4][4].position
    board.pawn_positions["white"] = board.board[4][5].position
    board.placePawns()
    
    print(board.printBoard())
    
    white_pawn_adjacent = opposingPawnAdjacent('black', board.board, board.board[4][4])
    black_pawn_adjacent = opposingPawnAdjacent('white', board.board, board.board[4][5])
    
    print(white_pawn_adjacent)
    assert white_pawn_adjacent[0] == True and white_pawn_adjacent[1].position == (4, 5)
    assert black_pawn_adjacent[0] == True and black_pawn_adjacent[1].position == (4, 4)