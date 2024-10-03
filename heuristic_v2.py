from variables import RED, ROUND, WHITE, SQUARE, PIECESTOWIN, ROWS, COLS
from grid import Grid

def evalSquare(piece, player):
    """Evaluate a single piece for the given player."""
    count = 0.0

    if piece is None:
        return 0.01
    
    if piece.get_color() == player:
        count += 0.2
    else:
        count -= 0.2
    
    if (piece.get_shape() == ROUND and player == WHITE) or (piece.get_shape() == SQUARE and player == RED):
        count += 0.4
    else:
        count -= 0.4
    
    return count

def evalBoard(grid: Grid, player):
    """Evaluate the entire board for the given player."""
    punteggio = 0.0
    
    # Evaluate rows
    for r in range(ROWS):
        for c in range(COLS - (PIECESTOWIN - 1)):
            count = 0.0
            for c1 in range(c, c + PIECESTOWIN):
                piece = grid.get_cell(r, c1)
                count += evalSquare(piece, player)
            punteggio += count
    
    # Evaluate columns
    for c in range(COLS):
        for r in range(ROWS - (PIECESTOWIN - 1)):
            count = 0.0
            for r1 in range(r, r + PIECESTOWIN):
                piece = grid.get_cell(r1, c)
                count += evalSquare(piece, player)
            punteggio += count

    # Evaluate main diagonals
    for r in range(ROWS - (PIECESTOWIN - 1)):
        for c in range(COLS - (PIECESTOWIN - 1)):
            count = 0.0
            for r1, c1 in zip(range(r, r + PIECESTOWIN), range(c, c + PIECESTOWIN)):
                piece = grid.get_cell(r1, c1)
                count += evalSquare(piece, player)
            punteggio += count

    # Evaluate secondary diagonals
    for r in range(ROWS - 1, ROWS - PIECESTOWIN, -1):
        for c in range(COLS - (PIECESTOWIN - 1)):
            count = 0.0
            for r1, c1 in zip(range(r, r - PIECESTOWIN, -1), range(c, c + PIECESTOWIN)):
                piece = grid.get_cell(r1, c1)
                count += evalSquare(piece, player)
            punteggio += count

    return punteggio

def evalPieces(pieces, player):
    """Evaluate the number of remaining pieces for the given player."""
    player_round = pieces[player][ROUND]
    player_square = pieces[player][SQUARE]
    other_player = RED if player == WHITE else WHITE
    other_player_round = pieces[other_player][ROUND]
    other_player_square = pieces[other_player][SQUARE]
    
    punteggio = 0.0

    if player == WHITE:
        punteggio += player_round - other_player_square
    else:
        punteggio += player_square - other_player_round

    return punteggio

def evalPosition(piece, player, r,c):
    
    count = 0.0

    if piece is None:
        count = checkRowCol(r,c)
        return count
    
    """if piece.get_color() == player:
        count += 2*checkRowCol(r,c)
    else:
        count -= 2*checkRowCol(r,c)
    
    if (piece.get_shape() == ROUND and player == WHITE) or (piece.get_shape() == SQUARE and player == RED):
        count += 4*checkRowCol(r,c)
    else:
        count -= 4*checkRowCol(r,c)"""
    
    return count

def checkRowCol(r,c):
    count = 0
    if r in {2, 3}:
        count += 1
    if c == 3:
        count += 2
    if r > 3:
        count -= 4
    if c in {0, 6}:
        count -= 1

    return count

def evalBoard_Position(grid: Grid, player):
    """Evaluate the entire board for the given player."""
    punteggio = 0.0
    
    # Evaluate rows
    for r in range(ROWS):
        for c in range(COLS - (PIECESTOWIN - 1)):
            count = 0.0
            for c1 in range(c, c + PIECESTOWIN):
                piece = grid.get_cell(r, c1)
                count += evalPosition(piece, player, r,c1)
            punteggio += count
    
    # Evaluate columns
    for c in range(COLS):
        for r in range(ROWS - (PIECESTOWIN - 1)):
            count = 0.0
            for r1 in range(r, r + PIECESTOWIN):
                piece = grid.get_cell(r1, c)
                count += evalPosition(piece, player, r1,c)
            punteggio += count

    # Evaluate main diagonals
    for r in range(ROWS - (PIECESTOWIN - 1)):
        for c in range(COLS - (PIECESTOWIN - 1)):
            count = 0.0
            for r1, c1 in zip(range(r, r + PIECESTOWIN), range(c, c + PIECESTOWIN)):
                piece = grid.get_cell(r1, c1)
                count += evalPosition(piece, player,r1,c1)
            punteggio += count

    # Evaluate secondary diagonals
    for r in range(ROWS - 1, ROWS - PIECESTOWIN, -1):
        for c in range(COLS - (PIECESTOWIN - 1)):
            count = 0.0
            for r1, c1 in zip(range(r, r - PIECESTOWIN, -1), range(c, c + PIECESTOWIN)):
                piece = grid.get_cell(r1, c1)
                count += evalPosition(piece,player, r1,c1)
            punteggio += count

    return punteggio

def wholeGrid(grid: Grid, player):
    """Evaluate the entire board for the given player."""
    count = 0.0
    
    # Evaluate rows
    for r in range(ROWS):
        for c in range(COLS):
            piece = grid.get_cell(r,c)
            count += checkRowCol(r,c)
            count += evalSquare(piece,player)
    
    return count


def heuristic(grid: Grid, player, pieces):
    #Euristica 1: Sola valutazione della posizione
    boardval = evalBoard(grid, player)
    return boardval + 0*evalPieces(pieces, player)

def heuristic2(grid: Grid, player, pieces):
    #Euristica 2: Solo valutazione dei pezzi
    return 4*evalPieces(pieces, player)

def heuristic3(grid: Grid, player, pieces):
    #Euristica 3: Valutazione della posizione + valutazione dei pezzi
    boardval = evalBoard(grid, player)
    return boardval + 4*evalPieces(pieces, player)

def heuristic4(grid: Grid, player, pieces):
    #Euristica 4: Valutazione della posizione con forte penalizzazione per colonne marginali
    boardval = wholeGrid(grid, player)
    return boardval

