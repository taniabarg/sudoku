dialogue = "s: save, q: quit, l:load \n"
A = dialogue + "Player A enter a move: "
B = dialogue + "Player B enter a move: "
sizes = [4, 9, 16]

def play():
    ''' (None) --> (None)

    Play a two-player sudoku game where players must fill the grid one number at
    a time without inputting a number that is already in that cluster, row or
    column. Game ends when there are no valid moves left or the grid is full.
    Grid size must be inputted by the user.
    '''
    global size
    global grid
    global player
    grid = []
    valid = False
    player = A
    size = int(input("Enter a grid size (N). "))
    while size not in sizes:
        print("You have entered an invalid grid size!")
        size = int(input("Enter a grid size again. "))
    print(show())
    while check_win() == 0:
        while not valid:        # Whenever move is not valid, asks for another
            m = input(player)
            if m == "q":
                return
            elif m == "s":
                save()
                continue
            elif m == "l":
                load()
                move = ""
                break
            else:
                move = m.split(",")
                row, column, value = int(move[0]), int(move[1]), int(move[2])
                valid = check_move(row, column, value)
        if check_win() != 0:    # Checks if loaded game is already complete
            break
        elif move == "":   # move hasn't been made after loading; restart loop
            continue
        # Changing players
        if player == A:
            player = B
        elif player == B:
            player = A
        grid[row][column] = value
        print(show())
        valid = False
    if check_win() == 1:
        if player == B:     # B ran out of moves, A wins
            print("Player A has won the game!")
        elif player == A:   # vice versa
            print("Player B has won the game!")
    elif check_win() == 2:
        print("It's a tie!")
    save()
    return
    
def show():
    ''' (None) --> (str)

    Return an NxN grid with root(N) x root(N) square clusters, where each cluster
    contains N numbers. Grid is intially a nested list and is returned as a special
    string format. Inital grid is comprised of all 0's and is constantly
    edited by the user through the function play().
    '''
    global sqr
    sqr = int(size**0.5)
    dash = 2 * size * "-" + "\n"
    grid_str = ""
    if grid == []:
        for i in range(size):
            grid.append([0]*size)
    countA, countB, countC = 0, 0, 0
    for x in range(size):       # These loops create a string depicting the grid
        for y in range(size):       
            grid_str += str(grid[x][y]) + " "
            countA += 1
            if countA == sqr:
                grid_str = grid_str.rstrip() + "|"
                countA = 0
                countB += 1
            if countB == sqr:
                grid_str = grid_str.rstrip("|") + "\n"
                countB = 0
                countC += 1
            if countC == sqr:
                grid_str += dash
                countC = 0
    grid_str = grid_str.rstrip().rstrip("-").rstrip()
    return grid_str

def check_move(row, column, value):
    ''' (int, int, int) --> (bool)

    Return False if the move initialized by the user in play() is invalid and
    True if it is valid. An invalid move is defined as targeting a square that
    already has a value, entering an out-of-range value, or entering a value
    that already exists in that row, column or cluster.
    '''
    column_list = []    
    cluster_list = []   # Creates a list of numbers in that column and cluster.
    if (row > size - 1) or (column > size - 1) or (value > size):
        return False    # Checks if out-of-range (1st condition)
    for rows in range(size):
        column_list.append(grid[rows][column])
    col_bound = column - (column % sqr)
    row_bound = row - (row % sqr)
    for a in range(sqr):
        for b in range(sqr):
            cluster_list.append(grid[row_bound + a][col_bound + b])
    if (grid[row][column] != 0) or \
       (value in grid[row]) or (value in column_list) or (value in cluster_list):
        return False    # Checks other two conditions
    else:
        return True

def check_win():
    ''' (None) --> (int)

    Return an integer corresponding to the status of the game in play(). A value
    of 0 means the game should continue, 1 means there is a clear winner (i.e.
    one player has run out of moves), and 2 means there is a tie (i.e. the grid
    is full).
    '''
    zero = False
    for row in range(size):
        for column in range(size):
            if grid[row][column] == 0:  # Checks if the grid is not full (there
                zero = True             #     are still zeroes left).
            for value in range(1, size + 1):
                if check_move(row, column, value):
                    return 0            # i.e. valid moves still exist
    if not zero:    
        return 2    # i.e. full grid
    else:
        return 1    # i.e. no valid moves left
                    
def save():
    ''' (None) --> (None)

    Save the current play() game grid to a file. User must enter file name.
    '''
    file_name = str(input("What would you like to name your save file? "))
    file = open(file_name + ".txt", 'w')
    file.write(show())
    file.close()
    return

def load():
    ''' (None) --> (None)

    Load a previously saved game from a save file by creating an associated
    nested list to be used in the functions show() and play(). This function
    will also determine whose turn the game left off at.
    '''
    global player
    file_name = str(input("What is the name of your previous save file? "))
    file = open(file_name + ".txt", 'r')
    nextline = file.readline()
    row = 0
    nonzero = 0
    while nextline != "":
        while row < size:
            if "-" not in nextline:
                # The following splits each line into a matrix row.
                grid[row] = nextline.replace("|", " ").split()
                for column in range(size):
                    grid[row][column] = int(grid[row][column])
                    if grid[row][column] != 0:
                        nonzero += 1    # Counts nonzero entries
                row += 1
            print(nextline.rstrip())
            nextline = file.readline()
    file.close()
    if nonzero % 2 == 0:
        player = A          # Even number of moves = player A's turn
    else:
        player = B          # Odd number of moves = player B's turn
    return

if __name__ == "__main__":
    play()
