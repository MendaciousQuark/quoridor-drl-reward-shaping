from game.move import Move
from utils.directions import UP, DOWN, LEFT, RIGHT
from errors.move_location_error import MoveLocationError
from errors.move_format_error import MoveFormatError

import pytest

def test_init():
    #whit move
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert move.colour == 'white'
    assert move.start == (8, 4)
    assert move.end == (7, 4)
    assert move.action == "move"
    assert move.direction == UP
    assert move.jumpDirection == None
    assert move.orientation == None
    
    #black move
    move = Move(False, "e1", "e2", "move", "up", None, None)
    assert move.colour == 'black'
    assert move.start == (8, 4)
    assert move.end == (7, 4)
    assert move.action == "move"
    assert move.direction == UP
    assert move.jumpDirection == None
    assert move.orientation == None
    
def test_parseColour():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert move.parseColour(True) == "white"
    assert move.parseColour(False) == "black"
    
    with pytest.raises(MoveFormatError):
        move.parseColour(None)
    
    with pytest.raises(MoveFormatError):
        move.parseColour("string")
    
def test_parseLocation():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert move.parseLocation("e1") == (8, 4)
    assert move.parseLocation("e2") == (7, 4)
    
    with pytest.raises(MoveLocationError):
        move.parseLocation("e10")
    
    with pytest.raises(MoveLocationError):
        move.parseLocation("e0")
    
    with pytest.raises(MoveLocationError):
        move.parseLocation("e")
    
    with pytest.raises(MoveLocationError):
        move.parseLocation("e1e2")

def test_parseAction():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert move.parseAction("move") == "move"
    assert move.parseAction("jump") == "jump"
    assert move.parseAction("place") == "place"
    
    with pytest.raises(MoveFormatError):
        move.parseAction("string")
    
    with pytest.raises(MoveFormatError):
        move.parseAction(None)
        
def test_parseOrientation():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    
    assert move.parseOrientation('h') == 'horizontal'
    assert move.parseOrientation('horizontal') == 'horizontal'
    assert move.parseOrientation('v') == 'vertical'
    assert move.parseOrientation('vertical') == 'vertical'
    
    with pytest.raises(MoveFormatError):
        move.parseOrientation('string')
    
    with pytest.raises(MoveFormatError):
        move.parseOrientation(None)
    
def test_parseDirection():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    
    assert move.parseDirection('u') == UP
    assert move.parseDirection('up') == UP
    assert move.parseDirection('d') == DOWN
    assert move.parseDirection('down') == DOWN
    assert move.parseDirection('l') == LEFT
    assert move.parseDirection('left') == LEFT
    assert move.parseDirection('r') == RIGHT
    assert move.parseDirection('right') == RIGHT
    
    with pytest.raises(MoveFormatError):
        move.parseDirection('string')
    
    with pytest.raises(MoveFormatError):
        move.parseDirection(None)

def test_move_str():
    move = Move(True, "e1", "e2", "move", "up", None, None)
    assert str(move) == f"Colour: {move.colour}\nAction: {move.action}\nStart: {move.start}\nEnd: {move.end}\nDirection: {move.direction}\nOrientation: {move.orientation}, jumpDirection: {move.jumpDirection}  "
    
def test_eq():
    move1 = Move(True, "e1", "e2", "move", "up", None, None)
    move2 = Move(True, "e1", "e2", "move", "up", None, None)
    move3 = Move(False, "e1", "e2", "move", "up", None, None)
    assert move1 == move2
    assert move1 != move3
    assert move2 != move3
    assert move1 != "string"
    assert move1 != None
    assert move1 != 1
    assert move1 != 1.0
    assert move1 != (1, 2)
    assert move1 != [1, 2]
    assert move1 != {"key": "value"}