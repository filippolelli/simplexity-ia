from collections import namedtuple

from variables import COLOURS, ROWS, SHAPES_EXT,COLS

Move=namedtuple("Move","column, shape")
def human_player(state):
    while(True):
        raw = input("Prossima mossa ("+COLOURS[state.to_move]+"):")
        mossa = raw.strip().split()
        if (len(mossa) != 2):
            print("Formato mossa errato, riprova")
            continue
        if (not mossa[0].isdigit() or not mossa[1].isdigit()):
            print("Il numero della colonna/del pezzo devono essere interi, riprova")
            continue
        col = int(mossa[0])-1
        shape=int(mossa[1])
        if (col < 0 or col > COLS-1):
            print("Colonna non esistente, riprova")
            continue
        if (shape>1 or shape<0):
            print("Pezzo non esistente, riprova")
            continue
        
        if (not state.grid.get_square(0,col).is_empty()):
            print("Colonna già piena, riprova")
            continue
        
        if (state.pieces[state.to_move][shape] == 0):
            print("Hai terminato i pezzi",SHAPES_EXT[shape]," ! Riprova")
            continue

        break  
    return Move(shape=shape,column=col)
