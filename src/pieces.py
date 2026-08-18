# white pieces will be denoted by uppercase letters and black by lowercase

EMPTY = "."

WHITE = "w"
BLACK = "b"

PIECES = {
    "k" : "king",
    "q" : "queen",
    "r" : "rook",
    "b" : "bishop",
    "n" : "knight",
    "p" : "pawn",
}

def color_of(piece):
    if piece == EMPTY:
        return None
    return WHITE if piece.isupper() else BLACK

def opponent(color):
    return BLACK if color == WHITE else WHITE

def is_friend(color, piece):
    return piece != EMPTY and color_of(piece) == color

def is_enemy(color, piece):
    return piece != EMPTY and color_of(piece) == opponent(color)


