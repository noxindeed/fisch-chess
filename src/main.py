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

