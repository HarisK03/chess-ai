"""
Minimax algorithm to find the best chess move from a given board state.
"""

from typing import Tuple

import chess
import chess.polyglot
import random
import time

"""
Piece evaluation tables.
"""

pawn_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5, -10,  0,  0, -10, -5,  5,
    5, 10, 10, -20, -20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

knight_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -90, -30, -30, -30, -30, -90, -50
]

bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0, 10, 10, 10, 10,  0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -20, -10, -90, -10, -10, -90, -10, -20
]

rook_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

queen_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0, -10,
    -10,  0,  5,  0,  0,  0,  0, -10,
    -20, -10, -10, 70, -5, -10, -10, -20
]

king_table = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

king_endgame_table = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]


class Minimax:
    """
    Perform a search using the Minimax algorithm.
    """
    transposition_table = {}
    book = chess.polyglot.open_reader("komodo.bin")

    def minimax(self, board: chess.Board, depth: int, alpha: int, beta: int, maxPlayer: bool) -> int:
        """
        Perform the minimax algorithm given a depth.
        """
        fen = board.fen()

        if fen in self.transposition_table:
            return self.transposition_table[fen]

        if depth == 0 or board.is_game_over():
            score = self.evaluate(board)
            self.transposition_table[fen] = score
            return score

        elif maxPlayer:
            best_score = float('-inf')
            for move in board.legal_moves:
                new_board = board.copy()
                new_board.push(move)
                score = self.minimax(new_board, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            self.transposition_table[fen] = best_score
            return best_score

        else:
            best_score = float('inf')
            for move in board.legal_moves:
                new_board = board.copy()
                new_board.push(move)
                score = self.minimax(new_board, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            self.transposition_table[fen] = best_score
            return best_score

    def evaluate(self, board: chess.Board) -> int:
        """
        Evaluate the board and return the evaluation.
        """
        if board.is_checkmate() and board.turn == chess.WHITE:
            return float('-inf')
        elif board.is_checkmate() and board.turn == chess.BLACK:
            return float('inf')

        qw = qb = rw = rb = bw = bb = nw = nb = pw = pb = 0
        pieces = board.piece_map().values()

        for piece in pieces:
            if piece.color == chess.WHITE:
                if piece.piece_type == chess.QUEEN:
                    qw += 1
                elif piece.piece_type == chess.ROOK:
                    rw += 1
                elif piece.piece_type == chess.BISHOP:
                    bw += 1
                elif piece.piece_type == chess.KNIGHT:
                    nw += 1
                elif piece.piece_type == chess.PAWN:
                    pw += 1
            else:
                if piece.piece_type == chess.QUEEN:
                    qb += 1
                elif piece.piece_type == chess.ROOK:
                    rb += 1
                elif piece.piece_type == chess.BISHOP:
                    bb += 1
                elif piece.piece_type == chess.KNIGHT:
                    nb += 1
                elif piece.piece_type == chess.PAWN:
                    pb += 1

        whiteMaterial = 9 * qw + 5 * rw + 3 * nw + 3 * bw + 1 * pw
        blackMaterial = 9 * qb + 5 * rb + 3 * nb + 3 * bb + 1 * pb

        num_moves = len(board.move_stack)
        phase = 'o' if num_moves > 40 or whiteMaterial + blackMaterial < 28 else 'e'

        dw, db = self.findDoubledPawns(board)
        sw, sb = self.findBlockedPawns(board)
        iw, ib = self.findIsolatedPawns(board)

        eval = 900 * (qw - qb) + 500 * (rw - rb) + 330 * (bw - bb) + 320 * \
            (nw - nb) + 100 * (pw - pb) - 30 * (dw - db + sw - sb + iw - ib)
        eval += self.getPieceEvals(board, phase)

        return eval

    def findDoubledPawns(self, board: chess.Board) -> Tuple[int, int]:
        """
        Find and return the number of doubled pawns.
        """
        white_doubled_pawns = 0
        black_doubled_pawns = 0

        for file_index, file_name in enumerate(chess.FILE_NAMES):
            white_pawns_on_file = 0
            black_pawns_on_file = 0

            squares_on_file = [chess.square(file_index, rank)
                               for rank in range(8)]

            for square in squares_on_file:
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    if piece.color == chess.WHITE:
                        white_pawns_on_file += 1
                    else:
                        black_pawns_on_file += 1

            if white_pawns_on_file > 1:
                white_doubled_pawns += white_pawns_on_file - 1
            if black_pawns_on_file > 1:
                black_doubled_pawns += black_pawns_on_file - 1

        return white_doubled_pawns, black_doubled_pawns

    def findBlockedPawns(self, board: chess.Board) -> Tuple[int, int]:
        """
        Find and return the number of blocked pawns.
        """
        white_blocked_pawns = 0
        black_blocked_pawns = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                color = board.color_at(square)
                if color == chess.WHITE:
                    forward_square = square + 8
                else:
                    forward_square = square - 8
                if board.color_at(forward_square) != color and board.piece_at(forward_square):
                    if color == chess.WHITE:
                        white_blocked_pawns += 1
                    else:
                        black_blocked_pawns += 1

        return white_blocked_pawns, black_blocked_pawns

    def findIsolatedPawns(self, board: chess.Board) -> Tuple[int, int]:
        """
        Find and return the number of isolated pawns.
        """
        white_isolated_pawns = 0
        black_isolated_pawns = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                color = board.color_at(square)
                file_idx = chess.square_file(square)
                if file_idx == 0:
                    left_file = None
                    right_file = file_idx + 1
                elif file_idx == 7:
                    left_file = file_idx - 1
                    right_file = None
                else:
                    left_file = file_idx - 1
                    right_file = file_idx + 1
                adjacent_files = [left_file, right_file]
                adjacent_pawns = 0
                for adjacent_file in adjacent_files:
                    if adjacent_file is not None:
                        adjacent_square = chess.square(
                            adjacent_file, chess.square_rank(square))
                        adjacent_piece = board.piece_at(adjacent_square)
                        if adjacent_piece and adjacent_piece.piece_type == chess.PAWN and board.color_at(adjacent_square) == color:
                            adjacent_pawns += 1
                if adjacent_pawns == 0:
                    if color == chess.WHITE:
                        white_isolated_pawns += 1
                    else:
                        black_isolated_pawns += 1

        return white_isolated_pawns, black_isolated_pawns

    def getPieceEvals(self, board: chess.Board, phase: str) -> int:
        """
        Find and return the evaluation using the piece evaluation tables.
        """
        score = 0

        for rank in range(7, -1, -1):
            for file in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece is None:
                    continue
                if piece.color == chess.WHITE:
                    if piece == chess.PAWN:
                        score += pawn_table[7 - rank][file]
                    elif piece == chess.KNIGHT:
                        score += knight_table[7 - rank][file]
                    elif piece == chess.BISHOP:
                        score += bishop_table[7 - rank][file]
                    elif piece == chess.ROOK:
                        score += rook_table[7 - rank][file]
                    elif piece == chess.QUEEN:
                        score += queen_table[7 - rank][file]
                    elif piece == chess.KING:
                        if phase == 'o':
                            score += king_table[7 - rank][file]
                        else:
                            score += king_endgame_table[7 - rank][file]
                else:
                    if piece == chess.PAWN:
                        score -= pawn_table[rank][file]
                    elif piece == chess.KNIGHT:
                        score -= knight_table[rank][file]
                    elif piece == chess.BISHOP:
                        score -= bishop_table[rank][file]
                    elif piece == chess.ROOK:
                        score -= rook_table[rank][file]
                    elif piece == chess.QUEEN:
                        score -= queen_table[rank][file]
                    elif piece == chess.KING:
                        if phase == 'o':
                            score -= king_table[rank][file]
                        else:
                            score -= king_endgame_table[rank][file]

        return score

    def get_best_move(self, board: chess.Board, depth: int, maxPlayer: bool, max_time: int) -> chess.Move:
        """
        Return the best move from the given board state.
        """
        possible_moves = [entry.move for entry in self.book.find_all(board)]
        if possible_moves:
            random_move = random.choice(possible_moves)
            return random_move

        start_time = time.time()
        depth = 1
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        while time.time() - start_time < max_time:
            best_score = float('-inf') if maxPlayer else float('inf')
            for move in board.legal_moves:
                new_board = board.copy()
                new_board.push(move)
                score = self.minimax(new_board, depth - 1,
                                     alpha, beta, not maxPlayer)
                if maxPlayer:
                    if score > best_score:
                        best_score = score
                        best_move = move
                    alpha = max(alpha, best_score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
                    beta = min(beta, best_score)

            depth += 1

        return best_move
