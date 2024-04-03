def saveBoard(board, action_ID, pawns, file_path='src\models\ground_truth\ground_truth_0.txt'):
        '''for every cell need to save location, walls up and left, and occupant
        can just write to file in row so locatin information is not needed since we can enumarte when loading
        seperate cells by ',' and rows by '\n'
        need to store the action ID as well
        number of walld for each pawn and turn number

        so the file would look something like this:
        U_1L_1P1,U_2L_2P2,U_3L_3P3 ... U_9L_9P9
        .
        .
        .
        .
        .
        .
        .
        U_1L_1P1,U_2L_2P2,U_3L_3P3 ... U_9L_9P9

        ww = number of walls for white
        bw = number of walls for black
        t = turn number
        a = action ID

        where c is the cell, U is the wall up, L is the wall left, and P is the pawn represented by 0 1 and for wall present or not
        c doesn't need to be stored as cells seperated by commas and are in order

        '''
        with open(file_path, 'w') as file:
            for row in board.board:
                for cell in row:
                    wall_up_part = 1 if cell.has_wall_up else 0
                    wall_left_part = 1 if cell.has_wall_left else 0
                    file.write(f"{wall_up_part}{wall_left_part},")
                file.write('\n')

            file.write(f"wp = {pawns['white'].position}\n")
            file.write(f"ww = {pawns['white'].walls}\n")
            file.write(f"bp = {pawns['black'].position}\n")
            file.write(f"bw = {pawns['black'].walls}\n")
            file.write(f"t = {board.turn}\n")
            file.write(f"a = {action_ID}")