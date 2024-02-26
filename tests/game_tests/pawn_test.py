import pytest

from game.pawn import Pawn
from game.move import Move
from errors.move_location_error import MoveLocationError
from errors.move_format_error import  MoveFormatError

def test_pawn_init():
    # white pawn
    pawn = Pawn(True, 0, 0)
    assert pawn.colour == True
    assert pawn.move_dir == -1
    assert pawn.position == [0, 0]
    assert pawn.walls == 10
    
    #black pawn
    pawn = Pawn(False, 0, 0)
    assert pawn.colour == False
    assert pawn.move_dir == 1
    assert pawn.position == [0, 0]
    assert pawn.walls == 10
    
def test_valid_requestMoveInput(monkeypatch):
    pawn = Pawn(True, 0, 0)
    # Test move input for move
    monkeypatch.setattr('builtins.input', lambda x: "move up e1 e2")
    move1 = pawn.requestMoveInput()
    
    # Test move input for place
    monkeypatch.setattr('builtins.input', lambda x: "place vertical a1")
    move2 = pawn.requestMoveInput()
    
    # Test move input for jump
    monkeypatch.setattr('builtins.input', lambda x: "jump e1 e3 up")
    move3 = pawn.requestMoveInput()
    
    # repeat for black pawn
    black_pawn = Pawn(False, 0, 0)
    
    # Test move input for move
    monkeypatch.setattr('builtins.input', lambda x: "move up e1 e2")
    move4 = black_pawn.requestMoveInput()
    
    # Test move input for place
    monkeypatch.setattr('builtins.input', lambda x: "place vertical a1")
    move5 = black_pawn.requestMoveInput()
    
    # Test move input for jump
    monkeypatch.setattr('builtins.input', lambda x: "jump e1 e3 up")
    move6 = black_pawn.requestMoveInput()
    
    # assert that moves are as expected
    assert move1 == Move(True, "e1", "e2", "move", "up", None, None)
    assert move2 == Move(True, "a1", None, "place", None, None, "vertical")
    assert move3 == Move(True, "e1", "e3", "jump", "up", "up", None)
    assert move4 == Move(False, "e1", "e2", "move", "up", None, None)
    assert move5 == Move(False, "a1", None, "place", None, None, "vertical")
    assert move6 == Move(False, "e1", "e3", "jump", "up", "up", None)
    
def test_invalid_colour_request(monkeypatch):
    # Invalid colour (no colour)
    neutral_pawn = Pawn(None, 0, 0)
    monkeypatch.setattr('builtins.input', lambda x: "move up e1 e2")
    with pytest.raises(MoveFormatError):
        neutral_pawn.requestMoveInput()    
    
def test_invalid_move_request(monkeypatch):
    # Setup for testing invalid inputs
    pawn = Pawn(True, 0, 0)

    # Invalid move input (no direction)
    monkeypatch.setattr('builtins.input', lambda x: "move e1 e2")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()

    # Invalid move input (no start/end)
    monkeypatch.setattr('builtins.input', lambda x: "move up e2")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()

    # Invalid move input (no start and end)
    monkeypatch.setattr('builtins.input', lambda x: "move up")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()

    # invalid move input (wrong start and end format)
    monkeypatch.setattr('builtins.input', lambda x: "move up 1 e2")
    with pytest.raises(MoveLocationError):
        pawn.requestMoveInput()
    
    # invalid move input (wrong start and end format)
    monkeypatch.setattr('builtins.input', lambda x: "move up e1 1")
    with pytest.raises(MoveLocationError):
        pawn.requestMoveInput()
    
    # Invalid move input (no action)
    monkeypatch.setattr('builtins.input', lambda x: "e1 e2")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
        
    # Invalid move input (extra information)
    monkeypatch.setattr('builtins.input', lambda x: "move up e1 e2 extra")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
    
def test_invalid_place_request(monkeypatch):
    pawn = Pawn(True, 0, 0)
    
    # Invallid place input (no orientation)
    monkeypatch.setattr('builtins.input', lambda x: "place a1")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
        
    # Invalid place input (no location)
    monkeypatch.setattr('builtins.input', lambda x: "place vertical")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
        
    # Invalid place input (no action)
    monkeypatch.setattr('builtins.input', lambda x: "vertical a1")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
        
    # Invalid place input (wrong location format)
    monkeypatch.setattr('builtins.input', lambda x: "place vertical 1")
    with pytest.raises(MoveLocationError):
        pawn.requestMoveInput()
        
    # Invalid place input (wrong orientation format)
    monkeypatch.setattr('builtins.input', lambda x: "place 1 a1")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
        
    # invalid place input (extra information)
    monkeypatch.setattr('builtins.input', lambda x: "place vertical a1 extra")
    with pytest.raises(MoveFormatError):
        pawn.requestMoveInput()
    

    
    