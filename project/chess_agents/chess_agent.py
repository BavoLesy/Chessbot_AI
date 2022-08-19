from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.utility import Utility
import time
import random

import os
import chess.polyglot
import chess.syzygy


def opening_move(board):
    # Read all possible moves from the opening book and pick one at random
    move = None
    moves = []
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, '../data/openings/performance.bin')
    with chess.polyglot.open_reader(file) as book:
        for entry in book.find_all(board):
            moves.append(entry.move)
    if moves:
        move = random.choice(moves)
    return move


def endgame_move(board):
    best_move = board.legal_moves.random_choice()
    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, '../data/syzygy')
    with chess.syzygy.open_tablebase(directory) as tb:
        distance_to_zero = tb.get_dtz(board)  # Distance to Zeroing
        win_draw_loss = tb.get_wdl(board)  # Win/Draw/Loss information (2,1,0,-1,-2)

    for move in board.legal_moves:
        piece_captured = board.piece_at(move.to_square)
        board.push(move)
        with chess.syzygy.open_tablebase(directory) as tb:
            new_win_draw_loss = tb.get_wdl(board)  # Win/Draw/Loss information (2,1,0,-1,-2)
            new_distance_to_zero = tb.get_dtz(board)  # Distance to Zeroing
        board.pop()
        if win_draw_loss == 0:
            if new_win_draw_loss == -2:
                return move
            elif new_win_draw_loss == -1:
                best_move = move
            elif new_win_draw_loss == 0:
                best_move = move
        if win_draw_loss == 1 or win_draw_loss == 2:
            if new_win_draw_loss == -2 or new_win_draw_loss == -1:
                if move.from_square.piece == chess.PAWN or piece_captured:  # If the move is a pawn or a capture, it is a good move
                    return move
                else:
                    if abs(new_distance_to_zero) <= abs(distance_to_zero):
                        distance_to_zero = new_distance_to_zero
                        best_move = move
        if win_draw_loss == -1 or win_draw_loss == -2:
            if new_win_draw_loss == -2 or new_win_draw_loss == -1 or new_win_draw_loss == 0:
                return move
            else:
                if abs(new_distance_to_zero) >= abs(distance_to_zero):
                    distance_to_zero = new_distance_to_zero
                    best_move = move
    return best_move


class ChessAgent(Agent):
    # Initialize your agent with whatever parameters you want
    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        super().__init__(utility,
                         time_limit_move - 0.5)  # Time limit - 0.5, so we have time for our program and no accidental taking too long
        self.name = "Search Agent"
        self.author = "B. Lesy & O. Rommens"
        self.opening = True  # True at the start of the game
        self.transposition_table = {}  # Transposition table for storing the values of the board

    def calculate_move(self, board: chess.Board):
        start_time = time.time()
        best_move = chess.Move.null()
        # at the start of the game, we want to use the opening book
        if self.opening:
            best_move = opening_move(board)
            if not best_move:  # If we have no more possible moves, end the usage of the opening book
                self.opening = False
        if not self.opening:
            if sum(board.piece_map()) <= 5:
                closing_move = endgame_move(board)
                return closing_move
            best_move = self.iterative_deepening(board, start_time)
            if board.is_irreversible(best_move):  # If the move is reversible, we clear out the transposition table because earlier entries are not valid anymore
                self.transposition_table.clear()
        print("This move took " + str(time.time() - start_time) + " seconds")
        return best_move

    def iterative_deepening(self, board, start_time):
        # Check our current position in the transposition table as to avoid unnecessary calculations
        key = chess.polyglot.zobrist_hash(board)  # Get the hash of the board (current position)
        if key in self.transposition_table:
            tt_score, tt_move = self.transposition_table[key]
            return tt_move  # Return the move from the transposition table if we have it

        # If we don't have it, we calculate the best move using negamax with alpha-beta pruning and iterative deepening
        alpha = -100000
        beta = 100000
        depth = 2
        best_score = -99999
        best_move = chess.Move.null()
        while time.time() < (start_time + self.time_limit_move) and depth < 6:  # If we still have time, we continue to search deeper
            for move in board.legal_moves:
                if time.time() - start_time > self.time_limit_move:
                    break
                board.push(move)
                score = -self.negamax_alphabeta(board, -beta, -alpha, depth, start_time)
                if score > best_score:
                    best_score = score
                    best_move = move
                if score > alpha:
                    alpha = score
                board.pop()
            depth += 1

        # Store the best move in the transposition table
        self.transposition_table[key] = (best_score, best_move)
        # print(self.transposition_table)
        return best_move


    def negamax_alphabeta(self, board, alpha, beta, depth, start_time):
        # Check our current position in the transposition table as to avoid unnecessary calculations
        key = chess.polyglot.zobrist_hash(board)  # Get the hash of the board (current position)
        if key in self.transposition_table:
            tt_score = self.transposition_table[key][0]
            return tt_score
        best_score = -9999
        best_move = chess.Move.null()
        if depth == 0:
            return self.quiescence(board, alpha, beta, start_time)  # self.utility.board_value(board)
        for move in board.legal_moves:
            if time.time() - start_time > self.time_limit_move:
                break
            board.push(move)
            score = -self.negamax_alphabeta(board, -beta, -alpha, depth - 1, start_time)
            board.pop()
            # Alpha beta pruning
            if score >= beta:
                return score
            if score > best_score:
                best_score = score
                best_move = move
            if score > alpha:
                alpha = score
        # Store the best move in the transposition table
        self.transposition_table[key] = (best_score, best_move)
        return best_score

    def quiescence(self, board, alpha, beta, start_time):
        score = self.utility.board_value(board)
        if score >= beta:
            return score
        if alpha < score:
            alpha = score
        for move in board.legal_moves:
            if time.time() - start_time > self.time_limit_move:
                break
            if board.is_capture(move):
                board.push(move)
                score = -self.quiescence(board, -beta, -alpha, start_time)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha
