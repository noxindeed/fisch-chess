from .pieces import EMPTY, WHITE, BLACK, color_of, opponent

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# directions and offsets for mvmt 
KNIGHT_OFFSETS = [
    (-2,-1), (-2,1),(-1,-2),(-1,2),(1,-2),(1,2),
    (2,-1),(2,1),
]

KING_OFFSETS = [
    (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1),

]

BISHOP_DIRECTIONS = [(-1,-1),(-1,1),(1,-1),(1,1)]
ROOK_DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1)]

QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + ROOK_DIRECTIONS

def on_board(row, col):
    return 0 <= row < 8 and 0 <= col < 8

def square_name(r,c):
    # converts (r,c) to algebraic names 
    return chr(ord("a")+c) + str(8-r)

def parse_square(name):
    # converts algebraic names to row,col pair
    if len(name) != 2:
        return None

    file_ch, rank_ch = name[0], name[1]
    if file_ch < "a" or file_ch > "h" or rank_ch < "1" or rank_ch > "8":
        return None
    return (8-int(rank_ch), ord(file_ch) - ord("a"))

class Board:
    def __init__(self):
        self.grid = [[EMPTY]*8 for _ in range(8)]

    def get(self, row, col):
        return self.grid[row][col]

    def set(self, row,col,piece):
        self.grid[row][col] = piece

    def find_king(self, color):
        target = "K" if color == WHITE else "k"
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] == target:
                    return (row,col)
        return None

    
