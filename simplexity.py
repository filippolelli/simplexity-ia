from collections import namedtuple
import copy
import math
from check import *
from variables import *
from grid import Grid, Piece
from heuristic_v2 import *

Move = namedtuple("Move", 'column, shape')
GameState = namedtuple('GameState', 'to_move, utility, pieces, grid')

class Simplexity:
    """A class to represent the Simplexity game, its states, and rules."""

    def __init__(self, r=6, c=7, k=4):
        self.r = r
        self.c = c
        self.k = k
        self.initial = GameState(
            to_move=WHITE,
            pieces={
                WHITE: {ROUND: N_ROUND, SQUARE: N_SQUARE},
                RED: {ROUND: N_ROUND, SQUARE: N_SQUARE}
            },
            grid=Grid(rows=r, cols=c),
            utility=0
        )

    def actions(self, state):
        """Return a list of legal moves from the current state."""
        columns = (c for c in range(self.c) if state.grid.get_empty_row(c) >= 0)  # Column is valid if not full
        pieces = [shape for shape in (ROUND, SQUARE) if state.pieces[state.to_move][shape] > 0]  # Valid shapes if any remain
        moves = []
        
        sorted_columns = sorted(columns, key=lambda col: abs(col - math.floor(self.c / 2)))
        
        for c in sorted_columns:
            for p in pieces:
                moves.append(Move(column=c, shape=p))
        
        return moves
    
    def to_move(self, state):
        """Return the player whose turn it is to move."""
        return state.to_move

    def result(self, state, move):
        """Return the resulting game state after a move."""
        grid = copy.deepcopy(state.grid)
        pieces = copy.deepcopy(state.pieces)
        piece = Piece(state.to_move, move.shape)
        row = grid.make_move(move.column, piece)
        pieces[state.to_move][move.shape] -= 1
        next_player = RED if state.to_move == WHITE else WHITE
        utility = self.compute_utility(grid, pieces, (row, move.column), player=next_player)
        return GameState(to_move=next_player, grid=grid, pieces=pieces, utility=utility)

    def utility(self, state, player):
        """Return the utility of the state for the given player."""
        return state.utility if player == WHITE else -state.utility

    def available_pieces(self, state, player):
        """Return the available pieces for the given player."""
        return state.pieces[player]

    def terminal_test(self, state):
        """Return True if the game is over, otherwise False."""
        return state.utility == 100000 or state.utility == -100000 or len(self.actions(state)) == 0

    def compute_utility(self, grid, pieces, move, player):
        """Compute the utility of the game state."""
        result = check_win(grid, move)
        if result[0] == WHITE:
            return 100000
        elif result[0] == RED:
            return -100000   

        result = heuristic(grid, player, pieces)

        """if player == WHITE:
            #in realtà rosso, motore vede 1 player avanti
            result = heuristic(grid, player, pieces)
        else:
            #in realtà bianco, motore vede 1 player avanti
            result = heuristic4(grid, player, pieces)"""
        

        return result if player == WHITE else -result

    def display(self, state):
        """Print or otherwise display the state."""
        print(state.grid)

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

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
