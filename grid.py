from variables import COLOURS, EMPTY, RED, SHAPES


class Grid:
    def __init__(self,r=6,c=7):
        self.matrix=[[Square() for _ in range(c)] for _ in range(r)]
        self.heights=[r-1 for _ in range(c)]
    def __str__(self):
        result="\n"
        for row in range(len(self.matrix)):
            for square in self.matrix[row]:
                result+=square.__str__()
            result+="\n"
        return result
    def get_square(self,r,c):
        return self.matrix[r][c]
    def set_square(self,r,c,piece):
        
        self.matrix[r][c].set_piece(piece)
        self.matrix[r][c].empty=False
    def make_move(self,c,piece):
        r=self.get_row_empty(c)
        if r<0:
            return r
        self.matrix[r][c].set_piece(piece)
        self.matrix[r][c].empty=False
        self.heights[c]-=1
        return r
    def get_matrix(self):
        return self.matrix

    def get_row_empty(self,col):
        return self.heights[col]
    
class Square:
    def __init__(self,piece=None):
        if(piece):
            self.empty=False
            self.piece=piece
        else:
            self.empty=True
    def __str__(self):
        if(self.empty):
            return f"\033[94m{EMPTY}\033[0m"
        else:
            if(self.piece.get_color()==RED):
                return f" \033[91m{SHAPES[self.piece.get_shape()]}\033[0m "
            return f" {SHAPES[self.piece.get_shape()]} "

    def is_empty(self):
        return self.empty
    def get_piece(self):
        if( not self.is_empty()):
            return self.piece
        return None
    def set_piece(self,piece):
        if(self.is_empty()):
            self.piece=piece
        return None