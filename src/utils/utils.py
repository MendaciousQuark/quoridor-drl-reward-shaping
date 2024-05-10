from .directions import UP, DOWN, LEFT, RIGHT, getDirectionIndex
import os
import re
import shutil

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
    #Join the chunks together without newline characters
    return ''.join([''.join(chunk) for chunk in chunks])

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
    try:
        if 0 <= number <= 8:
            # Convert the number to the corresponding lowercase letter
            letter = chr(ord('a') + number)
            return letter
        else:
            raise ValueError(f"Invalid number: {number}. Must be in the range 0 to 8.")
    except TypeError:
        raise ValueError(f"Invalid number: {number}. Must be an integer.")
    
def findPawn(colour, board):
    pawn_to_find = 'white' if colour else 'black'
    for row in board:
        for cell in row:
            if(cell.occupant is None):
                continue
            elif(cell.occupant == pawn_to_find):
                return cell
    raise ValueError(f"Could not find {pawn_to_find} pawn on the board.")

def locationToCell(i , j , board):
    if(validLocation(i, j)):
        return board[i][j]
    else:
        raise ValueError(f"Invalid location: ({i}, {j}). Must be in the range (0, 0) to (8, 8).")

def opposingPawnAdjacent(colour, board, center_cell):
    opposing_pawn_colour = 'black' if colour == 'white' else 'white'
    for direction in [UP, DOWN, LEFT, RIGHT]:
        location_to_check = getDirectionIndex(center_cell.position, direction)
        if(validLocation(*location_to_check)):
            if(board[location_to_check[0]][location_to_check[1]].occupant == opposing_pawn_colour):
                return (True, locationToCell(*location_to_check, board))
        else:
            continue
    return (False, None)

def get_next_file_number(directory_path, common_name_prefix):
    file_pattern = re.compile(rf'^{common_name_prefix}(\d+)')
    max_number = 0
    for filename in os.listdir(directory_path):
        match = file_pattern.match(filename)
        if match:
            current_number = int(match.group(1))
            if current_number > max_number:
                max_number = current_number
    return max_number + 1

def get_next_directory_number(directory_path, common_name_prefix):
    dir_pattern = re.compile(rf'^{common_name_prefix}(\d+)$')
    max_number = 0
    for entry in os.listdir(directory_path):
        if os.path.isdir(os.path.join(directory_path, entry)):
            match = dir_pattern.match(entry)
            if match:
                current_number = int(match.group(1))
                if current_number > max_number:
                    max_number = current_number
    return max_number + 1

def delete_previous_generations(directory_path):
    # Assuming the common prefix for directories is 'gen_'
    common_name_prefix = 'gen_'
    
    # Find out the next directory number, then calculate the latest generation number
    next_gen_number = get_next_directory_number(directory_path, common_name_prefix)
    latest_gen_number = next_gen_number - 2 #keep the last two generations
    
    # Compile the directory pattern for matching
    dir_pattern = re.compile(rf'^{common_name_prefix}(\d+)$')
    
    # List and filter directories in the specified path
    for entry in os.listdir(directory_path):
        if os.path.isdir(os.path.join(directory_path, entry)):
            match = dir_pattern.match(entry)
            if match:
                current_gen_number = int(match.group(1))
                # Delete the directory if it's not the latest generation
                if current_gen_number < latest_gen_number:
                    dir_to_delete = os.path.join(directory_path, entry)
                    shutil.rmtree(dir_to_delete)
                    print(f"Deleted: {dir_to_delete}")