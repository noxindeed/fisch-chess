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
DRAW_REPETITON = "draw_repetition"

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

    

    
            