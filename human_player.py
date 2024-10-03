from collections import namedtuple
from variables import ROUND, COLS, SQUARE

Move = namedtuple("Move", "column, shape")

def human_player(state):
    """Prompts the human player to make a move and validates the input."""
    while True:
        # Prompt the player for input
        raw = input(f"Prossima mossa ({state.to_move}): ").strip()
        parts = raw.split()

        # Validate input format
        if len(parts) != 2:
            print("Formato mossa errato, riprova.")
            continue
        
        col_str, shape = parts
        
        # Validate column input
        if not col_str.isdigit():
            print("Formato mossa errato, riprova.")
            continue
        
        col = int(col_str) - 1
        
        if col < 0 or col >= COLS:
            print("Colonna non esistente, riprova.")
            continue
        
        # Validate shape input
        if shape not in (SQUARE, ROUND):
            print("Formato mossa errato, riprova.")
            continue
        
        # Check if column is full
        if state.grid.get_empty_row(col) == -1:
            print("Colonna già piena, riprova.")
            continue
        
        # Check if the player has the selected shape
        if state.pieces[state.to_move][shape] == 0:
            print(f"Hai terminato i pezzi {shape}! Riprova.")
            continue
        
        #break
        # If all checks pass, return the move
        print(col)
        print(shape)
        return Move(column=col, shape=shape)
