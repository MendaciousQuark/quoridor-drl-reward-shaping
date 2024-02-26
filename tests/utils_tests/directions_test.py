from utils.directions import *
from game.cell import Cell

import pytest

def test_constaants():
    assert UP == (-1, 0)
    assert DOWN == (1, 0)
    assert LEFT == (0, -1)
    assert RIGHT == (0, 1)

def test_getDirectionIndex():
    assert getDirectionIndex((0, 0), UP) == [-1, 0]
    assert getDirectionIndex((0, 0), DOWN) == [1, 0]
    assert getDirectionIndex((0, 0), LEFT) == [0, -1]
    assert getDirectionIndex((0, 0), RIGHT) == [0, 1]
    
def test_getCellDirection():
    #warning: test uses cells that would be off the board. This is fine for testing purposes.
    
    start_cell = Cell(0, 0)
    target_cell = Cell(0, 1)
    assert getCellDirection(target_cell, start_cell) == RIGHT
    
    target_cell = Cell(0, -1)
    assert getCellDirection(target_cell, start_cell) == LEFT
    
    target_cell = Cell(1, 0)
    assert getCellDirection(target_cell, start_cell) == DOWN
    
    target_cell = Cell(-1, 0)
    assert getCellDirection(target_cell, start_cell) == UP
    
    target_cell = Cell(1, 1)
    with pytest.raises(ValueError):
        print(getCellDirection(target_cell, start_cell))
        getCellDirection(target_cell, start_cell)
    
def test_distance():
    assert distance((0, 0), (0, 0)) == 0
    assert distance((0, 0), (0, 1)) == 1
    assert distance((0, 0), (1, 0)) == 1
    assert distance((0, 0), (1, 1)) == 2
    assert distance((0, 0), (1, 2)) == 3
    assert distance((0, 0), (2, 2)) == 4
    assert distance((0, 0), (2, 3)) == 5
    assert distance((0, 0), (3, 3)) == 6
    assert distance((0, 0), (3, 4)) == 7
    assert distance((0, 0), (4, 4)) == 8
    assert distance((0, 0), (4, 5)) == 9
    assert distance((0, 0), (5, 5)) == 10
    assert distance((0, 0), (5, 6)) == 11
    assert distance((0, 0), (6, 6)) == 12
    assert distance((0, 0), (6, 7)) == 13
    assert distance((0, 0), (7, 7)) == 14
    assert distance((0, 0), (7, 8)) == 15
    assert distance((0, 0), (8, 8)) == 16
    assert distance((0, 0), (8, 9)) == 17
    assert distance((0, 0), (9, 9)) == 18
    assert distance((0, 0), (9, 10)) == 19
    assert distance((0, 0), (10, 10)) == 20
    assert distance((0, 0), (10, 11)) == 21
    assert distance((0, 0), (11, 11)) == 22
    assert distance((0, 0), (11, 12)) == 23
    assert distance((0, 0), (12, 12)) == 24