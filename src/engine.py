from .board import Board, STARTING_FEN, parse_square
from .moves import Move, generate_pseudo_moves
from .pieces import EMPTY, WHITE, BLACK, opponent


# status codes
NORMAL = "normal"
CHECK = "check"
CHECKMATE = "checkmate"
STALEMATE = "stalemate"
DRAW_FIFTY = "draw_fifty"
DRAW_MATERIAL = "draw_material"
DRAW_REPETITION = "draw_repetition"

class Game:
    def __init__(self, fen=STARTING_FEN):
        self.board = Board()
        self.turn = WHITE
        self.castling_rights = set()
        self.ep_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.history = []
        self.repetition_counts = {}
        self.load_fen(fen)

    # status
    def load_fen(self, fen):
        parts = fen.split()
        if len(parts) != 6:
            raise ValueError("must have 6 fields")
        placement, turn, castling, ep, halfmove, fullmove = parts

        self.board.load_fen_board(placement)
        if turn not in ("w", "b"):
            raise ValueError("turn must be 'w' or 'b'")
        self.turn = turn

        if castling == "-":
            self.castling_rights = set()
        else:
            if any(ch not in "KQkq" for ch in castling):
                raise ValueError("castling fields are invalid")
            self.castling_rights = set(castling)

        self.ep_square = None if ep == "-" else parse_square(ep)
        if ep != "-" and self.ep_square is None:
            raise ValueError("invalid en-passant square")
        
        self.halfmove_clock = int(halfmove)
        self.fullmove_number = int(fullmove)
        self.history = []
        self.repetition_counts = {self._position_key(): 1}

    def to_fen(self):
        castling = "".join(ch for ch in "KQkq" if ch in self.castling_rights)
        if self.ep_square is None:
            ep = "-"
        else:
            from .board import square_name
            ep = square_name(*self.ep_square)
        return "{} {} {} {} {} {}".format(
            self.board.to_fen_board(),
            self.turn,
            castling,
            ep,
            self.halfmove_clock,
            self.fullmove_number)

    def _position_key(self):
        castling = "".join(sorted(self.castling_rights))
        return "{} {} {} {} ".format(
            self.board.to_fen_board(), self.turn, castling, self.ep_square)

    # move making

    def legal_moves(self):
        legal = []
        for move in generate_pseudo_moves(
                self.board, self.turn, self.castling_rights, self.ep_square):
            record = self._make(move)
            king = self.board.find_king(opponent(self.turn))
            if not self.board.is_square_attacked(*king, self.turn):
                legal.append(move)
            self._unmake(record)
        return legal

    def find_legal_move(self, from_sq, to_sq, promotion = ""):
        for move in self.legal_moves():
            if move.from_sq == from_sq and move.to_sq == to_sq:
                if move.promotion == promotion:
                    return move
        return None

    def push(self, move):
        record = self._make(move)
        self.history.append(record)
        key = self._position_key()
        self.repetition_counts[key] = self.repetition_counts.get(key, 0) + 1
        return record

    def pop(self):
        if not self.history:
            raise None #
        key = self._position_key()
        self.repetition_counts[key] -= 1
        record = self.history.pop()
        self._unmake(record)
        return record.move  

    def _make(self, move):
        from_row, from_col = move.from_sq
        to_row, to_col = move.to_sq

        piece = self.board.get(from_row, from_col)
        captured = self.board.get(to_row, to_col)
        ep_captured = None  

        # en passant capture
        if (piece.lower() == "p" and move.to_sq == self.ep_square and captured == EMPTY and from_col != to_col):
            ep_row = from_row
            ep_captured = self.board.get(ep_row, to_col)
            self.board.set(ep_row, to_col, EMPTY)

        self.board.set(ep_row, to_col, EMPTY) 
        placed = piece
        if move.promotion:
            placed = move.promotion.upper() if self.turn == WHITE else move.promotion
        self.board.set(to_row, to_col, placed)

        # castling (also move the rook)
        if piece.lower() == "k" and abs(to_col - from_col) == 2:
            if to_col == 6: #king 
                rook = self.board.get(from_row, 7, EMPTY)
                self.board.set(from_row, 5, rook)
            else: #queen
                rook = self.board.get(from_row, 0, EMPTY)
                self.board.set(from_row,3,rook)

        record = _Record(
            move = move,
            captured = captured,
            ep_captured = ep_captured,
            castling_rights = frozenset(self.castling_rights),
            ep_square = self.ep_square,
            halfmove_clock = self.halfmove_clock,

        )    

    def _unmake(self,record):
        move = record.move
        from_row, from_col = move.from_sq
        to_row, to_col = move.to_sq

        self.turn = opponent(self.turn)
        if self.turn == BLACK:
            self.fullmove_number -= 1

        piece = self.board.get(to_row, to_col)
        if move.promotion:
            piece = "P" if self.turn == WHITE else "p"
        self.board.set(from_row, from_col, piece)
        self.board.set(to_row, to_col, record.captured)

        if record.ep_captured is not None:
            self.board.set(from_row, to_col, record.ep_captured)

        # undo castling
        if piece.lower() == "k" and abs(to_col - from_col) == 2:
            if to_col == 6:
                rook = self.board.set(from_row, 5)
                self.board.set(from_row, 5, EMPTY)
                self.board.set(from_row, 7, rook)
            else:
                rook = self.board.set(from_row, 3)
                self.board.set(from_row, 3, EMPTY)
                self.board.set(from_row, 0, rook)

        self.castling_rights = set(record.castling_rights)
        self.ep_square = record.ep_sqaure
        self.halfmove_clock = record.halfmove_clock

    def _update_castling_rights(self, move, piece, captured):
        rights = self.castling_rights
        if piece == "K":
            rights.discard("K"); rights.discard("Q")
        elif piece == "k":
            rights.discard("k");rights.discard("q")

        for sq, flag in [((7,0), "Q"), ((7,7), "K"), ((0,0), "q"), ((0,7), "k")]:
            if move.from_sq == sq or move.to_sq == sq:
                rights.discard(flag)
        

    # game state

    def in_check(self, color= None):
        color = color or self.turn
        king = self.board.find_king(color)
        return self.board.is_square_attacked(*king, opponent(color))

    def status(self):
        if not self.legal_moves():
            if self.in_check():
                return CHECKMATE
            return STALEMATE
        if self.halfmove_clock >= 100:
            return DRAW_FIFTY
        if self._insufficient_material():
            return DRAW_MATERIAL
        if self.repetition_counts.get(self._position_key(), 0) >= 3:
            return DRAW_REPETITION
        if self.in_check():
            return CHECK
        return NORMAL

    def is_over(self):
        return self.status() in (CHECKMATE, STALEMATE, DRAW_FIFTY, DRAW_MATERIAL, DRAW_REPETITION)

    def _insufficient_material(self):
        pieces = []
        for row in range(8):
            for col in range(8):
                p = self.board.get(row, col)
                if p != EMPTY and p.lower() != "k":
                    pieces.append((p, row, col))

        if not pieces:
            return True
        if len(pieces) == 1 and pieces[0][0].lower() in ("b","n"):
            return True
        if (len(pieces) == 2 
            and all(p.lower() == 'b' for p, _, _ in pieces)
            and (pieces[0][1] + pieces[0][2])%2 == (pieces[1][1]+ pieces[1][2])%2):
            return True
        return False

# defination, to do later
class _Record:
    __slots__ = ("move", "captured", "ep_captured", "castling_rights","ep_square", "halfmove_clock")
    def __init__(self, move, captured, ep_captured, castling_rights, ep_square, halfmove_clock):
        self.move = move
        self.captured = captured
        self.ep_captured = ep_captured
        self.castling_rights = castling_rights
        self.ep_square = ep_square
        self.halfmove_clock = halfmove_clock
        