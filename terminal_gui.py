import time
from simplexity import GameState, Simplexity, heuristic
from human_player import human_player
from ai_player import ai_player
from ai_player_no_cutoff import ai_player_no_cutoff
from monte_carlo_tree_search import ai_player_montecarlo
from ai_player_2 import ai_player_depth_5
from variables import *
from check import *
from grid import Piece


# Initialize the game
game = Simplexity()
state = game.initial

def print_board(grid):
    print(grid)  # Assuming the __str__ method in Grid provides the correct representation


def display_status(state):
    print(f"Hai a disposizione {state.pieces[state.to_move][SQUARE]} quadrati e {state.pieces[state.to_move][ROUND]} cerchi")
    print("Tocca al ", state.to_move)

def play_game():
    global state
    end = False
    aimoves = 0
    totaltime = 0

    while not end:
        display_status(state)
        
        if n == 2 or (n == 1 and state.to_move == WHITE):
            move = human_player(state)
        else:
            a = time.time()
            #if state.to_move == WHITE:
            move = ai_player(game,state)
            #else: move = ai_player(game, state)  # AI plays as RED for now
            b = time.time()
            print("Time to find move:", b - a, "s")
            totaltime += (b - a)
            aimoves += 1
        
        piece = Piece(state.to_move, move.shape)
        row = state.grid.make_move(move.column, piece)
        
        if row < 0:
            print("Mossa non valida, riprova.")
            continue
        
        state.pieces[state.to_move][move.shape] -= 1
        state = GameState(to_move=RED if state.to_move == WHITE else WHITE, grid=state.grid, pieces=state.pieces, utility=0)

        print_board(state.grid)
        
        result = check_win(state.grid, (row, move.column))
        if result[0] != -1:
            print(f"Ha vinto {result[0]}")
            end = True
        elif state.pieces[RED][ROUND] == 0 and state.pieces[RED][SQUARE] == 0:
            print("Pareggio")
            end = True

if __name__ == "__main__":
    while True:
        nplayer = input("Come vuoi giocare (1) contro AI o (2) 2 umani (3) 2 AI giocano una contro l'altra: ")
        stripped = nplayer.strip()
        if len(stripped.split()) != 1:
            print("Specifica il numero dei giocatori, riprova")
            continue
        if not stripped.isdigit():
            print("Il numero deve essere intero, riprova")
            continue
        n = int(stripped)
        if n < 1 or n > 3:
            print("Il numero deve essere o 1, 2 o 3, riprova")
            continue
        break

    play_game()
