from game.cell import Cell

def test_cell_init():
    cell = Cell(0, 0)
    assert cell.has_wall_up == False
    assert cell.has_wall_left == False
    assert cell.occupant == None
    assert cell.position == (0, 0)
    assert cell.neighbours == [None, [0, 1], None, [1,0]]
    
def test_setWalls():
    cell = Cell(0, 0)
    cell.setWalls(True, False)
    assert cell.has_wall_up == True
    assert cell.has_wall_left == False
    cell.setWalls(False, True)
    assert cell.has_wall_up == False
    assert cell.has_wall_left == True
    
def test_updateNeighbours():
    cell = Cell(0, 0)
    cell.position = (4, 4)
    cell.updateNeighbours()
    assert cell.neighbours == [[4, 3], [4, 5], [3, 4], [5, 4]]
    
def test_str_with_info():
    cell = Cell(0, 0)
    cell.setWalls(True, False)
    cell.occupant = "Player"
    assert str(cell) == "Walls: U\nPosition: (0, 0)\nOccupant: Player\nNeighbours: DR\n"

def test_copy():
    cell = Cell(8, 8)
    cell.setWalls(True, False)
    cell.occupant = "Player"
    new_cell = cell.copy()
    assert new_cell.has_wall_up == True
    assert new_cell.has_wall_left == False
    assert new_cell.occupant == "Player"
    assert new_cell.position == (8, 8)
    assert new_cell.neighbours == [[8,7], None, [7, 8], None]
    assert new_cell is not cell
    
def test_eq():
    a = Cell(0, 0)
    b = Cell(0, 0)
    c = a
    assert a == b == c