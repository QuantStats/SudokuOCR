import numpy as np

grid = None
solved_grid = None


def no_duplicate(ls):
    # remove zeros
    ls = [item for item in ls if item != 0]
    
    if len(ls) != len(set(ls)):
        return False
    
    return True


def valid():
    global grid
    
    # divisible by 3
    if grid.size % 3 != 0:
        print('Puzzle is not of a size divisible by 3.')
        return False
    
    for i in range(9):
        # check column (vertical)
        temp = grid[:, i]
        if no_duplicate(temp) is False:
            #print(f'Column {i} has duplicated entries.')
            return False
        
        # check row (horizontal)
        temp = grid[i, :]
        if no_duplicate(temp) is False:
            #print(f'Row {i} has duplicated entries.')
            return False
        
    # check 3 x 3 block
    ls = list(zip(range(0, 9, 3), range(0+3, 9+3, 3)))
    for i, j in ls:
        for x, y in ls:
            temp = grid[i:j, x:y].flatten()
            if no_duplicate(temp) is False:
                #print(f'Block[{i}:{j}, {x}:{y}] has duplicated entries.')
                return False
    return True


def feasible(y, x, n):
    global grid

    # check column (vertical)
    for i in range(9):
        if grid[y][i] == n:
            return False
    # check row (horizontal)
    for i in range(9):
        if grid[i][x] == n:
            return False

    # check within 3 x 3 grid
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0+i][x0+j] == n:
                return False

    return True


def solve():
    global grid
    global solved_grid
    
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if feasible(y, x, n):
                        # attempt to solve with a feasible value
                        grid[y][x] = n
                        # go back to the start with a reduced puzzle
                        solve()
                        # if a dead end is hit, set it to zero and try an alternative value
                        grid[y][x] = 0
                return # exit the recursion
    # if there are no zeroes left, print
    solved_grid = grid.copy()

