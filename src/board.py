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

# attack detection 

    def is_square_attacked(self, row, col, by_color):

        # pawns
        pawn = "P" if by_color == WHITE else "p"
        pawn_offset = 1 if by_color == WHITE else -1
        for dc in (-1, 1):
            r,c = row + pawn_offset, col+dc
            if on_board(r, c) and self.grid[r][c] == pawn:
                return True

        # knights
        knight = "N" if by_color == WHITE else "n"
        for dr, dc in KNIGHT_OFFSETS:
            r, c = row + dr, col + dc
            if on_board(r,c) and self.grid[r][c] == knight:
                return True 

        diagonals = ("B" if by_color == WHITE else "b",
                     "Q" if by_color == WHITE else "q")
        straights = ("R" if by_color == WHITE else "r",
                     "Q" if by_color == WHITE else "q")

        #kings 
        king = "K" if by_color == WHITE else "k"
        for dr,dc in KING_OFFSETS:
            r,c = row + dr, col + dc
            if on_board(r,c) and self.grid[r][c] == king:
                return True

        diagonals= (
            "B" if by_color == WHITE else "b",
            "Q" if by_color == WHITE else "q",
        )

        straights = (
            "R" if by_color == WHITE else "r",
            "Q" if by_color == WHITE else "q",
        )

        if self._ray_attacks(row, col, BISHOP_DIRECTIONS, diagonals):
            return True
        if self._ray_attacks(row, col, ROOK_DIRECTIONS, straights):
            return True 
        return False

    def _ray_attacks(self, row, col, directions, attackers):
        for dr, dc in directions:
            r,c = row+dr, col+dc
            while on_board(r,c):
                piece = self.grid[r][c]
                if piece != EMPTY:
                    if piece in attackers:
                        return True
                    break 
                r += dr
                c += dc
        return False

    # FEN

    def to_fen_board(self):
        rows = []
        for r in range(8):
            empty = 0
            out = ""
            for col in range(8):
                piece = self.grid[r][col]
                if piece == EMPTY:
                    empty += 1
                else:
                    if empty:
                        out += str(empty)
                        empty = 0
                    out += piece
            if empty:
                out += str(empty)
            rows.append(out)
        return "/".join(rows)

    def load_fen_board(self, placement):
        self.grid = [[EMPTY]*8 for _ in range(8)]
        ranks = placement.split("/")

        if len(ranks) != 8:
            raise ValueError("FEN board must have 8 ranks")
        for row, rank in enumerate(ranks):
            col = 0
            for ch in rank:
                if ch.isdigit():
                    col += int(ch)
                elif ch in "PNBRQKpnbrqk":
                    if col >= 8:
                        raise ValueError("FEN rank too long")
                    self.grid[row][col] = ch
                    col += 1
                else:
                    raise ValueError(f"Invalid FEN character: {ch!r}")
            if col != 8:
                raise ValueError("FEN rank too short")



        

        


