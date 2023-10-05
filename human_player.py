from collections import namedtuple

from variables import  ROUND, COLS, SQUARE

Move=namedtuple("Move","column, shape")
def human_player(state):
    while(True):
        raw = input("Prossima mossa ("+state.to_move+"):")
        mossa = raw.strip().split()
        if (len(mossa) != 2):
            print("Formato mossa errato, riprova")
            continue
        if (not mossa[0].isdigit() or (mossa[1]!=SQUARE and mossa[1]!=ROUND)):
            print("Formato mossa errato, riprova")
            continue
        col = int(mossa[0])-1
        shape=mossa[1]
        if (col < 0 or col > COLS-1):
            print("Colonna non esistente, riprova")
            continue
        
        if (not state.grid.get_square(0,col).is_empty()):
            print("Colonna già piena, riprova")
            continue
        
        if (state.pieces[state.to_move][shape] == 0):
            print("Hai terminato i pezzi",shape," ! Riprova")
            continue

        break  
    return Move(shape=shape,column=col)
