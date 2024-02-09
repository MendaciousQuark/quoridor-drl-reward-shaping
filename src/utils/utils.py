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

def moveLetterToNumber(letter):
    try:
        # Ensure the letter is lowercase to standardize the input
        letter = letter.lower()
    except AttributeError:
        raise ValueError(f"Invalid letter: {letter}. Must be a single character.")
    
    # 'a' maps to 0, 'b' to 1, ..., 'i' to 8
    number = ord(letter) - ord('a')
    # Check if the conversion is in the valid range [0-8]
    if 0 <= number <= 8:
        return number
    else:
        raise ValueError(f"Invalid letter: {letter}. Must be in the range 'a' to 'i'.")

def moveNumberToLetter(number):
    # Ensure the number is within the valid range [0-8]
    if 0 <= number <= 8:
        # Convert the number to the corresponding lowercase letter
        letter = chr(ord('a') + number)
        return letter
    else:
        raise ValueError(f"Invalid number: {number}. Must be in the range 0 to 8.")

def findPawn(colour, board):
    pawn_to_find = 'white' if colour else 'black'
    for row in board:
        for cell in row:
            if(cell.occupant is None):
                continue
            elif(cell.occupant == pawn_to_find):
                return cell

