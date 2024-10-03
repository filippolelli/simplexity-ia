import collections.abc
from grid import Piece, Grid
from variables import *

def check_row(grid, row, col):
    last_piece = grid.get_cell(row, col)
    player = last_piece.get_color()
    start = max(0, col - PIECESTOWIN + 1)
    end = min(COLS - 1, col + PIECESTOWIN - 1)
    return count(grid, row, range(start, end + 1), player)

def check_column(grid, row, col):
    last_piece = grid.get_cell(row, col)
    player = last_piece.get_color()
    start = max(0, row - PIECESTOWIN + 1)
    end = min(ROWS - 1, row + PIECESTOWIN - 1)
    return count(grid, range(start, end + 1), col, player)

def check_diagonals(grid, row, col):
    shift = PIECESTOWIN - 1
    last_piece = grid.get_cell(row, col)
    player = last_piece.get_color()
    
    # Calculate the four extreme points of the two diagonals
    a, b, c, d = (row - shift, col - shift), (row - shift, col + shift), (row + shift, col - shift), (row + shift, col + shift)
    
    # Calculate the distance of the points from the border
    da = max(0, -a[0] if -a[0] > -a[1] else -a[1])
    db = max(0, -b[0] if -b[0] > (b[1] - COLS + 1) else b[1] - COLS + 1)
    dc = max(0, c[0] - ROWS + 1 if (c[0] - ROWS + 1) > -c[1] else -c[1])
    dd = max(0, d[0] - ROWS + 1 if (d[0] - ROWS + 1) > (d[1] - COLS + 1) else d[1] - COLS + 1)
    
    # Points out of bounds are brought inside, those already inside are not modified because they have a distance of 0
    a, b, c, d = (a[0] + da, a[1] + da), (b[0] + db, b[1] - db), (c[0] - dc, c[1] + dc), (d[0] - dd, d[1] - dd)
    
    diagonals = []
    if length(b, c) >= PIECESTOWIN:
        diagonals.append([b, c])
    if length(a, d) >= PIECESTOWIN:
        diagonals.append([a, d])
    
    for diag in diagonals:
        start = diag[0]
        end = diag[1]
        step_column = 1 if start[1] <= end[1] else -1
        val = count(grid, range(start[0], end[0] + 1), range(start[1], end[1] + step_column, step_column), player)
        if val[0] != -1:
            return val
    return [-1,[]]

def check_win(grid, last_index):  # return winner else -1
    result = check_row(grid, last_index[0], last_index[1])
    if result[0] != -1:
        return result
    result = check_column(grid, last_index[0], last_index[1])
    if result[0] != -1:
        return result
    result = check_diagonals(grid, last_index[0], last_index[1])
    return result

def inside(point):
    return 0 <= point[0] < ROWS and 0 <= point[1] < COLS

def length(p1, p2):
    return abs(p1[1] - p2[1]) + 1

def count(grid, range_row, range_col, player):  #return [win(1) else -1, positions of pieces that aligned]
    if not isinstance(range_row, collections.abc.Iterable):
        range_row = [range_row] * len(range_col)
    elif not isinstance(range_col, collections.abc.Iterable):
        range_col = [range_col] * len(range_row)

    count_color = 0
    count_shape = {ROUND: 0, SQUARE: 0}
    winning=[]

    for r, c in zip(range_row, range_col):

        piece = grid.get_cell(r, c)
        if piece is None:  # If there's an empty space, skip it
            count_color = 0
            count_shape = {ROUND: 0, SQUARE: 0}
            winning=[]

            continue
        if piece.get_color() == player:
            count_color += 1
        else:
            count_color = 0
        count_shape[piece.get_shape()] += 1
        count_shape[ROUND if piece.get_shape() == SQUARE else SQUARE] = 0
        winning.append([r,c])
        if count_shape[ROUND] == PIECESTOWIN:
            return [WHITE,winning]
        if count_shape[SQUARE] == PIECESTOWIN:
            return [RED,winning]
        if count_color == PIECESTOWIN:
            return [player,winning]
    return [-1,[]]
