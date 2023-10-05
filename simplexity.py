from collections import namedtuple
import copy
import math
from checkers import checkWin
import numpy as np

from piece import Piece
from grid import Grid, Square
from human_player import Move
from variables import *

GameState=namedtuple('GameState','to_move , utility, pieces, grid ')
class Simplexity:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def __init__(self, r=6, c=7, k=4):
        self.r = r
        self.c = c
        self.k = k
        self.initial=GameState(to_move=WHITE,pieces={WHITE:{ROUND:N_ROUND, SQUARE: N_SQUARE},RED:{ROUND:N_ROUND, SQUARE: N_SQUARE}},grid=Grid(),utility=0)
    def actions(self, state):
        col=(c for c in range (0,self.c) if state.grid.get_row_empty(c)>=0) ###colonna ok se non piena
        pieces=list((shape for shape in (ROUND,SQUARE) if state.pieces[state.to_move][shape]>0)) ###shape ok se ne è rimasta almeno una
        moves=[]
        def sorting(colonna):
            return abs(colonna-math.floor(self.c/2))
        colnew=sorted(col,key=sorting)
        for c in colnew:
            for p in pieces:
                moves.append(Move(column=c, shape=p))
        return moves
    
    def to_move(self,state):
        return state.to_move
    def result(self, state, move):
        grid=copy.deepcopy(state.grid)
        pieces=copy.deepcopy(state.pieces)
        piece = Piece(move.shape,state.to_move)
        row=grid.make_move(move.column,piece)
        pieces[state.to_move][move.shape]-=1
        turn=RED if state.to_move==WHITE else WHITE
        return GameState(to_move=turn,grid=grid,pieces=pieces,utility=self.compute_utility(grid,pieces, (row,move.column),player=turn))

    def utility(self, state, player):
        return state.utility if player == WHITE else -state.utility
    def available_pieces(self,state,player):
        return state.pieces[player]

    def terminal_test(self, state):
        return state.utility == 100000 or state.utility == -100000 or len(self.actions(state)) == 0

    def compute_utility(self, grid:Grid,pieces, move,player): 
        
        result= checkWin(grid,move)
        if (result==WHITE):
            return 100000
        elif(result==RED):
            return -100000   

        
        result=heuristic(grid,player,pieces)

        if(player==WHITE):
            return result
        else:
            return -result
        
        
        
        
    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))



def evalSquare(square, player):
    
    count=0
    
    if(square.is_empty()):
        return 0.01
    if(square.get_piece().get_color()==player):
        count+=0.2
    else:
        count-=0.2
    if((square.get_piece().get_shape()==ROUND and player==WHITE) or (square.get_piece().get_shape()==SQUARE and player==RED)):
        count+=0.4  
    else:
        count-=0.4
        
                
    return count


def evalBoard(grid:Grid,player): 
    punteggio = 0
    
        # valutazione delle righe
    for r in range(ROWS):
        for c in range(COLS - (PIECESTOWIN-1)):
            count=0
            for c1 in range(c,c+PIECESTOWIN):
                count+=evalSquare(grid.get_square(r,c1),player)
    
            punteggio += count
    
    # valutazione delle colonne
    for c in range(COLS):
        for r in range(ROWS - (PIECESTOWIN-1)):
            ###print(f"checkColumns = r:{r},c:{c}")
            
            count=0
            for r1 in range(r,r+PIECESTOWIN):
                
                count+=evalSquare(grid.get_square(r1,c),player)
             
            punteggio += count

        # valutazione delle diagonali principali
    for r in range(ROWS - (PIECESTOWIN-1)):
        for c in range(COLS - (PIECESTOWIN-1)):
            count=0
            for r1,c1 in zip(range(r,r+PIECESTOWIN),range(c,c+PIECESTOWIN)):
                count+=evalSquare(grid.get_square(r1,c1),player)
            
            
            punteggio += count
   
    # valutazione delle diagonali secondarie
    for r in range(ROWS-1,ROWS-PIECESTOWIN,-1):
        for c in range(COLS - (PIECESTOWIN-1)):
            count=0
            for r1,c1 in zip(range(r,r-PIECESTOWIN,-1),range(c,c+PIECESTOWIN)):
                count+=evalSquare(grid.get_square(r1,c1),player)
            punteggio += count
  
    return punteggio

def evalPieces(pieces,player):
    player_round=pieces[player][ROUND]
    player_square=pieces[player][SQUARE]
    other_player_round=pieces[RED if player==WHITE else WHITE][ROUND]
    other_player_square=pieces[RED if player==WHITE else WHITE][SQUARE]
    punteggio = 0

    if(player ==WHITE):
        punteggio+=player_round-other_player_square
    else:
        punteggio+=player_square-other_player_round
    return punteggio

def heuristic(grid:Grid,player,pieces):
    boardval=evalBoard(grid,player)
    return (boardval+0*evalPieces(pieces,player))
