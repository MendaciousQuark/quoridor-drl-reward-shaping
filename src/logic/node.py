class Node:
    def __init__(self, neighbours = [], position = (0, 0), walls = []):
        self.parent = None
        self.neighbours = neighbours
        self.position = position
        self.walls = walls
        #traversal cost is the cost of moving from one node to another
        self.traversal_cost = 1
        #cost of the path from the start node to the current node (overriden by A* algorithm)
        self.path_cost = 0
        self.heuristic_cost = 0
        #heuristic cost is the distance from the node to the final row
        self.total_cost = 0
        
    def calcHeuristicCost(self, colour):
        if(colour):
            goal = (0, self.position[1])
        else:
            goal = (8, self.position[1])
        #heuristic cost is the manhattan distance from the node to the final row
        return abs(self.position[0] - goal[0]) + abs(self.position[1] - goal[1])
    
    def __str__(self):
        return f"Node at {self.position}, \nneighbours: {self.neighbours}, \nwalls: {self.walls}, \npath_cost: {self.path_cost}, \nheuristic_cost: {self.heuristic_cost}, \ntotal_cost: {self.total_cost}"

    def __eq__(self, other_node: object) -> bool:
        return self.position == other_node.position \
            and self.neighbours == other_node.neighbours \
            and self.walls == other_node.walls
