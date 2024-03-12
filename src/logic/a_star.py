import pdb

#graph is a 2D list of nodes, colour is a boolean, start is a tuple, end is a list of tuples
def aStar(graph, colour, start, end):
    #set all the heuristics based om the colour
    setheuristicCost(graph, colour)
    #Initialise the open and closed lists
    openList = []
    closedList = []
    
    #Initialise the start node
    startNode = graph[start[0]][start[1]]
    startNode.path_cost = 0
    startNode.heuristic_cost
    startNode.total_cost = startNode.path_cost + startNode.heuristic_cost
    openList.append(startNode)
    #While there are nodes in the open list
    while(len(openList) > 0):
        #Get the node with the lowest total_cost
        currentNode = openList[0]
        for node in openList:
            if(node.total_cost < currentNode.total_cost):
                currentNode = node
        #If the current node is the end node
        if(currentNode.position in end):
            #initialise the path
            path = []
            #Reconstruct the path
            while(currentNode.parent is not None):
                path.append(currentNode.position)
                currentNode = currentNode.parent
            #Add the start node to the path
            path.append(startNode.position)
            #Return the path (reverse before passing to get the correct order of the path)
            return path[::-1]
        
        #Remove the current node from the open list and add it to the closed list
        openList.remove(currentNode)
        closedList.append(currentNode)
        
        #For each neighbour of the current node
        for neighbour in currentNode.neighbours:
            #If the neighbour is in the closed list
            if(neighbour in closedList):
                continue
            #Calculate the traversal_value of the neighbour
            traversal_value = currentNode.path_cost + 1
            #If the neighbour is not in the open list
            if(neighbour not in openList):
                #Add the neighbour to the open list
                openList.append(neighbour)
            #If the traversal_value of the neighbour is greater than the traversal_value of the current node
            if(traversal_value >= neighbour.path_cost):
                # Set the parent of the neighbour to the current node
                neighbour.parent = currentNode
                # Set the path_cost of the neighbour
                neighbour.path_cost = traversal_value
                # Optionally, recalculate the heuristic_cost if it depends on the path
                # neighbour.heuristic_cost = calculateHeuristic(neighbour, end)
                # Set the total_cost of the neighbour
                neighbour.total_cost = neighbour.path_cost + neighbour.heuristic_cost
            #Set the parent of the neighbour to the current node
            neighbour.parent = currentNode
            #Set the traversal_value of the neighbour
            neighbour.path_cost = traversal_value
            #Set the h value of the neighbour
            neighbour.heuristic_cost
            #Set the total_cost of the neighbour
            neighbour.total_cost = neighbour.path_cost + neighbour.heuristic_cost
    #If there are no nodes in the open list, return an empty path
    print("\nNo path found\n")
    return []

def setheuristicCost(graph, colour):
    for row in graph:
        for node in row:
            node.heuristic_cost = node.calcHeuristicCost(colour)