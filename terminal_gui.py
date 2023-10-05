import time
from simplexity import GameState, Simplexity, heuristic
from human_player import human_player
from ai_player import ai_player

from variables import *
from checkers import *

game=Simplexity()

print("SIMPLEXITY")
print("Formato mossa: NUMERO_COLONNA(1-7) PEZZO(${ROUND}/${SQUARE})")
print()

while(True):
    nplayer=input("Come vuoi giocare (1) contro AI o (2) 2 umani (3) 2 AI giocano una contro l'altra: ")
    stripped=nplayer.strip()
    if (len(stripped.split()) != 1):
        print("Specifica il numero dei giocatori, riprova")
        continue
    if(not stripped.isdigit()):
        print("Il numero deve essere intero , riprova")
    n=int(stripped)    
    if(n<1 or n>3):
        print("Il numero deve essere o 1,2 o 3 , riprova")
        continue
    break


end = False
state=game.initial
aimoves=0
totaltime=0
while (not end):
    print(f"Hai a disposizione {state.pieces[state.to_move][SQUARE]} quadrati  e {state.pieces[state.to_move][ROUND]} cerchi ")
    print("Tocca al ",state.to_move)
    valutazione=heuristic(state.grid,state.to_move,state.pieces)
    if(state.to_move==WHITE):
            print("Valutazione:",valutazione)
    else:
        print("Valutazione:",-valutazione)
    if(n==2 or (n==1 and state.to_move==WHITE)):
        move=human_player(state)
    else:
        a=time.time()
        move=ai_player(game,state) ##AI gioca sempre con rosso per ora
        b=time.time()
        print("Time to find move:",b-a,"s")
        totaltime+=(b-a)
        aimoves+=1
    
    grid=state.grid
    pieces=state.pieces
    piece = Piece(move.shape,state.to_move)
    if pieces[state.to_move][move.shape]<=0:
        continue
    row=grid.make_move(move.column,piece)

    if(row < 0):
         continue
    pieces[state.to_move][move.shape]-=1
    state=GameState(to_move=RED if state.to_move==WHITE else WHITE,grid=grid,pieces=pieces,utility=0)

    print(state.grid)
    
    
    result= checkWin(state.grid, (row,move.column))
    if (result!=-1):
        print("Ha vinto ",result)
        end = True
        #print("Average time for AI move:",totaltime/aimoves,"s")
    if (state.pieces[RED][ROUND]==0 and state.pieces[RED][SQUARE]==0):
        print("Pareggio")
        end=True
    
    


