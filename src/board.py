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


