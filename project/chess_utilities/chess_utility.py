import chess
from project.chess_utilities.utility import Utility


class ChessUtility(Utility):
    def __init__(self) -> None:
        self.score = 0

    def board_value(self, board: chess.Board):
        return self.material_value(board) + self.king_safety(board, chess.WHITE) - self.king_safety(board, chess.BLACK)

    # Calculate the amount of white pieces minus the amount of black pieces, each with a given value (weight)
    def material_value(self, board: chess.Board):

        pawn_value = 100
        knight_value = 320
        bishop_value = 330
        rook_value = 500
        queen_value = 900
        n_white = 0
        n_white += len(board.pieces(piece_type=chess.PAWN, color=chess.WHITE)) * pawn_value
        n_white += len(board.pieces(piece_type=chess.BISHOP, color=chess.WHITE)) * bishop_value
        n_white += len(board.pieces(piece_type=chess.KNIGHT, color=chess.WHITE)) * knight_value
        n_white += len(board.pieces(piece_type=chess.ROOK, color=chess.WHITE)) * rook_value
        n_white += len(board.pieces(piece_type=chess.QUEEN, color=chess.WHITE)) * queen_value

        n_black = 0
        n_black += len(board.pieces(piece_type=chess.PAWN, color=chess.BLACK)) * pawn_value
        n_black += len(board.pieces(piece_type=chess.BISHOP, color=chess.BLACK)) * bishop_value
        n_black += len(board.pieces(piece_type=chess.KNIGHT, color=chess.BLACK)) * knight_value
        n_black += len(board.pieces(piece_type=chess.ROOK, color=chess.BLACK)) * rook_value
        n_black += len(board.pieces(piece_type=chess.QUEEN, color=chess.BLACK)) * queen_value
        return n_white - n_black

    # Mobility of the pawns is a measure of how many squares the pawn can move to
    def mobility(self, board: chess.Board, color: bool):
        mobility = 0
        for square in board.pieces(color, chess.PAWN):
            mobility = mobility + len(list(board.attackers(not color, square)))
        return mobility

    # King safety is a measure of how safe the king is
    def king_safety(self, board: chess.Board, color: bool):
        king_safety = 0
        king = board.king(color)
        if king is not None:
            next_to_king = self.next_to_king(board, color)
            for square in next_to_king:
                king_safety = king_safety + len(list(board.attackers(color, square)))
        return king_safety

    # Next to king is a list of squares next to the king. This is used to calculate king safety.
    # If there are pieces next to the king, the king is not safe
    def next_to_king(self, board: chess.Board, color: bool):
        king = board.king(color)
        next_to_king = []
        for square in chess.SquareSet(chess.BB_RANK_1 | chess.BB_RANK_8 | chess.BB_FILE_A | chess.BB_FILE_H):
            if square != king:
                if board.piece_at(square) is None:
                    next_to_king.append(square)
        return next_to_king


