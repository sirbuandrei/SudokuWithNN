import numpy as np
from random import shuffle, randint

grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
counter = 0
unsolved = 0


# GET THE NUMBER OF UNFILLED GRID VALUES TO KNOW WHEN THE GAME HAS FINISHED
def get_solved():
    global unsolved
    unsolved = 0
    for row in range(0,9):
        for col in range(0,9):
            if grid[row][col] == 0:
                unsolved += 1
    return unsolved


def solveGrid(grid):
    global counter
    # FIN NEXT EMPTY CELL
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                # CHECK THAT THIS VALUE HAS NOT ALREADY BE USED ON THIS ROW
                if not (value in grid[row]):
                    # CHECK THAT THIS VALUE HAS NOT ALREADY BE USED ON THIS COLUMN
                    if not value in (
                            grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col],
                            grid[6][col],
                            grid[7][col], grid[8][col]):
                        # IDENTIFY WHICH OF THE 9 SQUARES WE ARE WORKING ON
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        # CHECK THAT THIS VALUE HAS NOT ALREADY BE USED ON THIS 3X3 SQUARE
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if checkGrid(grid):
                                counter += 1
                                break
                            else:
                                if solveGrid(grid):
                                    return True
            break
    grid[row][col] = 0


def checkGrid(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False
    return True


# A BACKTRACKING/RECURSIVE FUNCTION TO CHECK ALL POSSIBLE COMBINATIONS OF NUMBERS UNTIL A SOLUTION IS FOUND
def fillGrid(grid):
    global counter
    # FIND NEXT EMPTY CELL
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            shuffle(numberList)
            for value in numberList:
                # CHECK THAT THIS VALUE HAS NOT ALREADY BE USED ON THIS ROW
                if not (value in grid[row]):
                    # CHECK THAT THIS VALUE HAS NOT ALREADY BE USED ON THIS COLUMN
                    if not value in (
                            grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col],
                            grid[6][col],
                            grid[7][col], grid[8][col]):
                        # IDENTIFY WHICH OF THE 9 SQUARES WE ARE WORKING ON
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        # CHECK THAT THIS VALUE HAS NOT ALREADY BE USED ON THIS 3X3 SQUARE
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if checkGrid(grid):
                                return True
                            else:
                                if fillGrid(grid):
                                    return True
            break
    grid[row][col] = 0


def get_grid():
    fillGrid(grid)
    global counter
    attempts = 5
    counter = 1
    while attempts > 0:
        # SELECT A RANDOM CELL THAT IS NOT ALREADY EMPTY
        row = randint(0, 8)
        col = randint(0, 8)
        while grid[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)
        # REMEMBER ITS CELL VALUE IN CASE WE NEED TO PUT IT BACK
        backup = grid[row][col]
        grid[row][col] = 0

        # TAKE A FULL COPY OF THE GRID
        copyGrid = []
        for r in range(0, 9):
            copyGrid.append([])
            for c in range(0, 9):
                copyGrid[r].append(grid[r][c])

        # COUNT THE NUMBER OF SOLUTIONS THAT THIS GRID HAS
        # (USING A BACKTRACKING APPROACH IMPLEMENTED IN THE SOLVEGRID() FUNCTION)
        counter = 0
        solveGrid(copyGrid)
        # IF THE NUMBER OF SOLUTION IS DIFFERENT FROM 1 THEN WE NEED TO CANCEL THE CHANGE BY PUTTING THE VALUE
        # WE TOOK AWAY BACK IN THE GRID
        if counter != 1:
            grid[row][col] = backup
            # WE COULD STOP HERE, BUT WE CAN ALSO HAVE ANOTHER ATTEMPT WITH A DIFFERENT CELL
            # JUST TO TRY TO REMOVE MORE NUMBERS
            attempts -= 1


def checkvalue(y, x, value):
    # CHECK FOR THE VALUE IN THE COL
    for i in range(0, 9):
        if grid[y][i] == value:
            return False
    # CHECK FOR THE VALUE IN THE ROW
    for i in range(0, 9):
        if grid[i][x] == value:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    # CHECK FOR THE VALUE IN THEE SQUARE
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == value:
                return False

    return True
