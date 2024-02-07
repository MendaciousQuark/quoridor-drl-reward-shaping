def validLocation(i, j):
        # Return True if the location is on the board, False if it's off the board
        return 0 <= i <= 8 and 0 <= j <= 8
    
def joinWithNewlines(lst, n):
    #Divide the list into chunks of size n
    chunks = [lst[i:i + n] for i in range(0, len(lst), n)]
    #Join the chunks together with newline characters
    return '\n'.join([''.join(chunk) for chunk in chunks])

def joinWithoutNewlines(lst, n):
    #Divide the list into chunks of size n
    chunks = [lst[i:i + n] for i in range(0, len(lst), n)]
    #Join the chunks together with newline characters
    return '\n'.join([''.join(chunk) for chunk in chunks])