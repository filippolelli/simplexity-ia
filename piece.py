class Piece:
    def __init__(self, shape, colour):
        self.shape = shape
        self.colour = colour
    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.shape == other.shape and self.colour == other.colour
        return False
    def eq_color(self,other):
        if isinstance(other, Piece):
            return self.colour == other.colour
    def eq_shape(self,other):
        if isinstance(other, Piece):
            return self.shape == other.shape
    def get_color(self):
        return self.colour
    def get_shape(self):
        return self.shape
    

