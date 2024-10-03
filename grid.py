from variables import RED, ROUND, WHITE, SQUARE

class Piece:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape

    def __repr__(self):
        if self.color == RED:
            return f"\033[91m{' O ' if self.shape == ROUND else ' X '}\033[0m"
        else:
            return f"{' O ' if self.shape == ROUND else ' X '}"
        
    def get_color(self):
        return self.color
    
    def get_shape(self):
        return self.shape
   

class Grid:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.matrix = [[None for _ in range(cols)] for _ in range(rows)]
        self.heights = [rows - 1 for _ in range(cols)]

    def __str__(self):
        result = "\n"
        for row in self.matrix:
            for cell in row:
                result += "\033[94m E \033[0m" if cell is None else str(cell)
            result += "\n"
        return result

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.matrix[row][col]
        raise IndexError("Cell out of bounds")

    def set_cell(self, row, col, piece):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.matrix[row][col] is None:
                self.matrix[row][col] = piece
            else:
                raise ValueError("Cell is already occupied")
        else:
            raise IndexError("Cell out of bounds")

    def make_move(self, col, piece):
        row = self.get_empty_row(col)
        if row < 0:
            return -1  # Column is full
        self.set_cell(row, col, piece)
        self.heights[col] -= 1
        return row

    def get_empty_row(self, col):
        if 0 <= col < self.cols:
            return self.heights[col]
        raise IndexError("Column out of bounds")

"""if __name__ == "__main__":
    grid = Grid()
    print(grid)

    piece1 = Piece(RED, ROUND)
    piece2 = Piece("white", "square")

    grid.make_move(0, piece1)
    grid.make_move(1, piece2)

    print(grid)"""