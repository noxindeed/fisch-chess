from __future__ import annotations

import os 
import random
import re
import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional

from .board import STARTING_FEN, parse_square, square_name
from .engine import (
    CHECK, CHECKMATE, STALEMATE, DRAW_FIFTY, DRAW_MATERIAL, DRAW_REPETITION, NORMAL, STALEMATE, Game, )

from .moves import Move, generate_pseudo_moves
from .pieces import EMPTY, WHITE, BLACK, color_of, opponent

RESET = "\033[0m"
DIM = "\033[2m"
ACCENT = "\033[92m"
ERROR = "\033[91m"
STATUS = "\033[32m"
CLEAR = "\033[2J\033[H"
USE_COLOR = sys.stdout.isatty() and os.enviorn.get("NO_COLOR") is None


PUZZLES = [
    {"fen": "6k1/5ppp/8/8/8/8/8/RK6 w - - 0 1", "solution": "a1a8", "text": "white to move; mate in 1"},
    {"fen": "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1", "solution": "h5f7", "text": "white to move; mate in 1"},
    {"fen": "3qk3/2b5/8/8/6b1/8/5PP1/6K1 b - - 0 1", "solution": "d8d1", "text": "black to move; mate in 1"},  
    {"fen": "7k/5B2/4NR2/8/8/8/8/6K1 w - - 0 1", "solution": "f6h6", "text": "white to move; mate in 1"},
]

PIECE_VALUE = {"p":100, "n":320, "b":330, "r":500, "q":900, "k":0}

