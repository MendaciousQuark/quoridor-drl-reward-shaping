from logic.node import Node

def test_init():
    n = Node()
    assert n.parent == None
    assert n.neighbours == []
    assert n.position == (0, 0)
    assert n.walls == []
    assert n.traversal_cost == 1
    assert n.path_cost == 0
    assert n.heuristic_cost == 0
    assert n.total_cost == 0
    
def test_calcHeuristicCost():
    n = Node()
    
    for i in range(9):
        n.position = (4, i)
        assert n.calcHeuristicCost('white') == 4
        assert n.calcHeuristicCost('black') == 4
        
        n.position = (0, i)
        
        assert n.calcHeuristicCost('white') == 0
        assert n.calcHeuristicCost('black') == 8
        
        n.position = (8, i)
        assert n.calcHeuristicCost('white') == 8
        assert n.calcHeuristicCost('black') == 0
        
        n.position = (i, 0)
        assert n.calcHeuristicCost('white') == i
        assert n.calcHeuristicCost('black') == 8-i
        
        n.position = (8-i, 8)
        assert n.calcHeuristicCost('white') == 8-i
        assert n.calcHeuristicCost('black') == i
        
        n.position = (3, i)
        assert n.calcHeuristicCost('white') == 3
        assert n.calcHeuristicCost('black') == 5
        
        n.position = (i, i)
        assert n.calcHeuristicCost('white') == i
        assert n.calcHeuristicCost('black') == 8-i

def test_str():
    node = Node()
    assert str(node) == "Node at (0, 0), \nneighbours: [], \nwalls: [], \npath_cost: 0, \nheuristic_cost: 0, \ntotal_cost: 0"
        