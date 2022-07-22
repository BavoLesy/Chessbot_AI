import chess
from project.chess_utilities.utility import Utility


class ChessUtility(Utility):

    def __init__(self) -> None:
        self.score = 0

    # Calculate the amount of white pieces minus the amount of black pieces
    def board_value(self, board: chess.Board):
        return self.material_value(board) + self.king_safety(board, chess.WHITE) - self.king_safety(board, chess.BLACK)

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


    def king_safety(self, board: chess.Board, color: bool):
        king_safety = 0
        king = board.king(color)
        if king is not None:
            next_to_king = self.next_to_king(board, color)
            for square in next_to_king:
                king_safety = king_safety + len(list(board.attackers(color, square)))
        return king_safety

