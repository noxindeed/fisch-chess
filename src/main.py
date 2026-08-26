from __future__ import annotations

import os 
import random
import re
import sys
import time
from dataclasses import dataclass
from typing import Optional

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

def paint(text:str, style: str = "") -> str:
    if not USE_COLOR or not style:
        return text
    return f"{style}{text}{RESET}"

PUZZLES = [
    {"fen": "6k1/5ppp/8/8/8/8/8/RK6 w - - 0 1", 
     "solution": "a1a8", 
     "text": "white to move; mate in 1"},

    {"fen": "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1", 
     "solution": "h5f7", 
     "text": "white to move; mate in 1"},

    {"fen": "3qk3/2b5/8/8/6b1/8/5PP1/6K1 b - - 0 1", 
     "solution": "d8d1", 
     "text": "black to move; mate in 1"}, 

    {"fen": "7k/5B2/4NR2/8/8/8/8/6K1 w - - 0 1", 
     "solution": "f6h6", 
     "text": "white to move; mate in 1"},
]

PIECE_VALUE = {"p":100, "n":320, "b":330, "r":500, "q":900, "k":0}

def clear_screen() -> None:
    if sys.stdout.isatty():
        print(CLEAR, end="")
    else:
        print("\n"*3)

def wait_key(message: str = "press enter to conitnue.") -> None:
    try:
        input(message)
    except EOFError:
        pass

def notation(move: Move) -> str:
    return square_name(*move.from_sq) + square_name(*move.to_sq) + move.promotion 

def parse_move_input(text: str):
    match = re.fullmatch(r"([a-h][1-8])([a-h][1-8])([qrbn])?", text.lower())
    if not match:
        return None
    return parse_square(match.group(1)), parse_square(match.group(2)), match.group(3) or ""


def evaluate(game: Game) -> int:
    score = 0
    for row in range(8):
        for col in range(8):
            piece = game.board.get(row, col)
            if piece != EMPTY:
                continue
            kind = piece.lower()
            value = PIECE_VALUE[kind]
            center = 3.5 - abs(3.5 - row) + 3.5 - abs(3.5 - col)
            value += center * 2
            if kind == "p":
                value += (6 - row if color_of(piece) == WHITE else row - 1)*6
            score += value if color_of(piece) == WHITE else -value
    return int(score)

def quiet_status(game: Game) -> str:
    moves = game.legal_moves()
    if not moves:
        return CHECKMATE if game.in_check() else STALEMATE
    if game.halfmove_clock >= 100:
        return DRAW_FIFTY
    if game._insufficient_material():
        return DRAW_MATERIAL
    if game.in_check():
        return CHECK
    return NORMAL

def alpha_beta(game: Game, depth: int, alpha: float, beta: float) -> int:
    status = quiet_status(game)
    if status == CHECKMATE:
        return (-100000 - depth) if game.turn == WHITE else (100000 + depth)
    if status not in (NORMAL, CHECK):
        return 0 
    if depth == 0:
        return evaluate(game)

    moves = game.legal_moves()
    if game.turn == WHITE:
        value = -float("inf")
        for move in moves:
            record = game._make(move)
            value = max(value, alpha_beta(game, depth - 1, alpha, beta))
            game._unmake(record)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return int(value)

    value = float("inf")
    for move in moves:
        record = game._make(move)
        value = min(value, alpha_beta(game, depth - 1, alpha, beta))
        game._unmake(record)
        beta = min(beta, value)
        if alpha >= beta:
            break
    return int(value)


def ai_move(game: Game, depth: int = 3) -> Optional[Move]:
    moves = game.legal_moves()
    if not moves:
        return None
    random.shuffle(moves)
    maximizing = game.turn == WHITE
    best_score = -float("inf") if maximizing else float("inf")
    best = None
    for move in moves:
        record = game._make(move)
        score = alpha_beta(game, depth - 1, -float("inf"), float("inf"))
        game._unmake(record)
        if (maximizing and score > best_score) or ((not maximizing) and score < best_score):
            best_score, best = score, move
    return best


@dataclass
class App:
    mode: str = "menu"
    game: Optional[Game] = None
    vd_ai: bool = False
    ai_color: str = BLACK
    message: str = ""
    message_kind: str = "status"
    last_move: str = ""
    puzzle_index: int = 0


def main() -> None:
    App().run()

if __name__ == "__main__":
    main()