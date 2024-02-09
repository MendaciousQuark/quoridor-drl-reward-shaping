def aStar(graph, colour, start, end):
    #Initialise the open and closed lists
    openList = []
    closedList = []
    
    #Initialise the start node
    startNode = graph[start[0]][start[1]]
    startNode.path_cost = 0
    startNode.heuristicCost(colour)
    startNode.total_cost = startNode.path_cost + startNode.heuristicCost(colour)
    openList.append(startNode)
    
    #While there are nodes in the open list
    while(len(openList) > 0):
        #Get the node with the lowest f value
        currentNode = openList[0]
        for node in openList:
            if(node.total_cost < currentNode.total_cost):
                currentNode = node
        
        #If the current node is the end node
        if(currentNode.position == end):
            #Initialise the path
            path = []
            #Reconstruct the path
            while(currentNode.parent is not None):
                path.append(currentNode.position)
                currentNode = currentNode.parent
            #Return the path
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
                continue
            #Set the parent of the neighbour to the current node
            neighbour.parent = currentNode
            #Set the traversal_value of the neighbour
            neighbour.path_cost = traversal_value
            #Set the h value of the neighbour
            neighbour.heuristicCost(colour)
            #Set the f value of the neighbour
            neighbour.total_cost = neighbour.path_cost + neighbour.heuristicCost(colour)
    #If there are no nodes in the open list, return an empty path
    return []