from dataclasses import dataclass

from .board import (
    KING_OFFSETS, KNIGHT_OFFSETS, BISHOP_DIRECTIONS, ROOK_DIRECTIONS, QUEEN_DIRECTIONS, on_board, square_name,

)

from .pieces import EMPTY, WHITE, color_of, is_enemy

PROMOTION_PIECES = "qrbn"

@dataclass
class Move:

    from_sq: tuple
    to_sq: tuple
    promotion: str = "" 

    def notation(self):
        text = square_name(*self.from_sq) + square_name(*self.to_sq)
        return text + self.promotion

    
def _pawn_push(from_row, from_col, to_row, to_col, last_row):
    if to_row == last_row:
        for promo in PROMOTION_PIECES:
            yield Move((from_row, from_col), (to_row, to_col), promo)
    else :
        yield Move((from_row, from_col), (to_row, to_col))



def _pawn_moves(board, row, col, color, ep_square):

    forward = -1 if color == WHITE else 1
    start_row = 6 if color == WHITE else 1
    last_row = 0 if color == WHITE else 7

    one = row + forward
    if on_board(one, col) and board.get(one, col) == EMPTY:
        yield from _pawn_push(row, col, one, col, last_row)
        two = row + 2 * forward
        if row == start_row and board.get(two, col) == EMPTY:
            yield Move((row, col), (two, col))
    for dc in (-1, 1):
        r,c = row + forward, col + dc
        if not on_board(r, c):
            continue
        if is_enemy(board.get(r, c), color):
            yield from _pawn_push(row, col, r, c, last_row)
        elif ep_square is not None and (r, c) == ep_square:
            yield Move((row, col), (r,c))

def _jump_moves(board,row,col,color,offsets):
    for dr, dc in offsets:
        r,c = row + dr, col + dc
        if not on_board(r,c):
            continue
        target = board.get(r,c)
        if target == EMPTY or is_enemy(target, color):
            yield Move((row, col), (r,c))

def _slide_moves(board, row, col, color, directions):
    for dr, dc in directions:
        r,c = row + dr, col + dc
        while on_board(r,c):
            target = board.get(r,c)
            if target == EMPTY:
                yield Move((row, col), (r,c))
            else:
                if is_enemy(target,color):
                    yield Move((row, col), (r,c))
                break
            r += dr
            c += dc


def _castle_moves(board, row, col, color, castling_rights):
    home_row = 7 if color == WHITE else 0

    if row != home_row or col != 4:
        return

    enemy = "b" if color == WHITE else "w"
    king_side = "K" if color == WHITE else "k"
    queen_side = "Q" if color == WHITE else "q"

    #king side, f and g empty and e f g not attacked 
    if king_side in castling_rights:
        if (board.get(home_row, 5) == EMPTY
                and board.get(home_row, 6) == EMPTY
                and board.get(home_row, 7).lower() == "r"
                and not board.is_square_attacked(home_row, 4, enemy)
                and not board.is_square_attacked(home_row, 5, enemy)
                and not board.is_square_attacked(home_row, 6, enemy)):
            yield Move((row, col), (home_row, 6))

    # queen side, sqrs b c d must be empty and e d c not attacked
    if queen_side in castling_rights:
        if (board.get(home_row, 3) == EMPTY
                and board.get(home_row, 2)== EMPTY
                and board.get(home_row, 1)== EMPTY
                and board.get(home_row, 0).lower()=="r"
                and not board.is_square_attacked(home_row, 4, enemy)
                and not board.is_square_attacked(home_row, 3, enemy)
                and not board.is_square_attacked(home_row, 2, enemy)):
            yield Move((row, col), (home_row, 2))


def generate_pseudo_moves(board, color, castling_rights, ep_square):

    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)
            if piece == EMPTY or color_of(piece) != color:
                continue
            kind = piece.lower()

            
            if kind == "p":
                yield from _pawn_moves(board, row, col, color, ep_square)
            elif kind == "n":
                yield from _jump_moves(board, row, col, color, KNIGHT_OFFSETS)
            elif kind == "b":
                yield from _slide_moves(board, row, col, color, BISHOP_DIRECTIONS)
            elif kind == "q":
                yield from _slide_moves(board, row, col, color, QUEEN_DIRECTIONS)
            elif kind == "k":
                yield from _jump_moves(board, row, col, color, KING_OFFSETS)
                yield from _castle_moves(board, row, col, color, castling_rights)
            elif kind == "r":
                yield from _slide_moves(board, row, col, color, ROOK_DIRECTIONS)
