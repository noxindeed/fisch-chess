from dataclasses import dataclass

from .board import (
    KING_OFFSETS, KNIGHT_OFFSETS, BISHOP_DIRECTIONS, ROOK_DIRECTIONS, QUEEN_DIRECTIONS, on_board, square_name,

)

from .pieces import EMPTY, WHITE, color_of, is_enemy

PROMOTIONS_PIECES = "qrbn"

