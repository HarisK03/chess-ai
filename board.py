from typing import Tuple

import chess as ch
import chess.polyglot
import pygame
import random
from minimax import Minimax
from constants import ROWS, COLS, SQUARE_SIZE, LIGHT, DARK, SELECT, POSSIBLE, FROM_MOVE, TO_MOVE


class Board:
    """
    The chess board representation.
    """
    IMAGES = {}
    SOUNDS = {}
    TABLE = {}
    MINIMAX = Minimax()

    def __init__(self) -> None:
        """
        Initiaze the board with the given parameters.
        """
        self.board = ch.Board()
        self.selected_piece = None
        self.selected_square = None
        self.previous_squares = None
        self.moves = {}
        self.human_turn = True
        self.book = chess.polyglot.open_reader("komodo.bin")
        self.load_images()
        self.load_sounds()

    def load_images(self) -> None:
        """
        Load the chess piece images.
        """
        pieces = ['wp', 'wn', 'wb', 'wr', 'wq',
                  'wk', 'bp', 'bn', 'bb', 'br', 'bq', 'bk']
        for piece in pieces:
            self.IMAGES[piece] = pygame.image.load('images/' + piece + '.png')

    def load_sounds(self) -> None:
        """
        Load the chess sounds.
        """
        pygame.mixer.init()
        sounds = ['capture', 'castle', 'check',
                  'checkmate', 'move', 'stalemate']
        for sound in sounds:
            self.SOUNDS[sound] = pygame.mixer.Sound('sfx/' + sound + '.mp3')

    def draw_board(self, win: pygame.display) -> None:
        """
        Draw the chess squares.
        """
        win.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT, (row * SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win: pygame.display, pos: Tuple[int, int]) -> None:
        """
        Draw the chess pieces on the board.
        """
        colors = {ch.WHITE: 'w', ch.BLACK: 'b'}
        types = {ch.PAWN: 'p', ch.KNIGHT: 'n', ch.BISHOP: 'b',
                 ch.ROOK: 'r', ch.QUEEN: 'q', ch.KING: 'k'}

        if self.selected_square is not None:
            ss_file = ch.square_file(self.selected_square)
            ss_rank = ch.square_rank(self.selected_square)

        if self.previous_squares is not None:
            pygame.draw.rect(win, FROM_MOVE, (ch.square_file(self.previous_squares[0]) * SQUARE_SIZE, (
                ROWS - ch.square_rank(self.previous_squares[0]) - 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, TO_MOVE, (ch.square_file(self.previous_squares[1]) * SQUARE_SIZE, (
                ROWS - ch.square_rank(self.previous_squares[1]) - 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for rank in range(ROWS):
            for file in range(COLS):
                square = ch.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    color = colors[piece.color]
                    type = types[piece.piece_type]
                    piece_image = self.IMAGES[color + type]
                    piece_image = pygame.transform.scale(
                        piece_image, (SQUARE_SIZE, SQUARE_SIZE))

                    if self.selected_square is None or file != ss_file or rank != ss_rank:
                        win.blit(piece_image, (file * SQUARE_SIZE,
                                 (ROWS - rank - 1) * SQUARE_SIZE))

        if self.selected_square is not None:
            color = colors[self.selected_piece.color]
            type = types[self.selected_piece.piece_type]

            # draw select background
            alpha = 200
            select_background = pygame.Surface(
                (SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            select_background.set_alpha(alpha)
            pygame.draw.rect(select_background, SELECT,
                             (0, 0, SQUARE_SIZE, SQUARE_SIZE))
            win.blit(select_background, (ss_file * SQUARE_SIZE,
                     (ROWS - ss_rank - 1) * SQUARE_SIZE))

            # draw shadow piece
            alpha = 128
            image = self.IMAGES[color + type].copy()
            image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            win.blit(image, (ss_file * SQUARE_SIZE,
                     (ROWS - ss_rank - 1) * SQUARE_SIZE))

            # draw moves background
            alpha = 150
            for move in self.board.legal_moves:
                if move.from_square == self.selected_square:
                    to_square = move.to_square
                    # default to promoting to queen
                    move.promotion = ch.QUEEN if move.promotion is not None else None
                    self.moves[ch.square_name(to_square)] = move

            for move in self.moves:
                to_square = ch.parse_square(move)
                to_square_file = ch.square_file(to_square)
                to_square_rank = ch.square_rank(to_square)
                move_background = pygame.Surface(
                    (SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                move_background.set_alpha(alpha)
                pygame.draw.rect(move_background, POSSIBLE,
                                 (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                win.blit(move_background, (to_square_file * SQUARE_SIZE,
                         (ROWS - to_square_rank - 1) * SQUARE_SIZE))

            # draw piece at cursor
            # 50 px to center on cursor
            win.blit(self.IMAGES[color + type], (pos[0] - 50, pos[1] - 50))

    def select_square(self, pos: Tuple[int, int], first_click: bool) -> None:
        """
        Select the square.
        """
        file, rank = pos[0] // SQUARE_SIZE, ROWS - (pos[1] // SQUARE_SIZE) - 1
        square = ch.square(file, rank)
        piece = self.board.piece_at(square)

        if self.human_turn and piece and (self.board.turn and piece.color == ch.WHITE or not self.board.turn and piece.color == ch.BLACK):
            if self.selected_square is None and piece is not None and first_click:
                self.selected_square = square
                self.selected_piece = piece

    def release_square(self, pos: Tuple[int, int], win: pygame.display) -> None:
        """
        Release piece at the square.
        """
        file, rank = pos[0] // SQUARE_SIZE, ROWS - (pos[1] // SQUARE_SIZE) - 1
        square = ch.square(file, rank)

        if ch.square_name(square) in self.moves:
            self.previous_squares = (self.selected_square, square)
            self.play_move_sound(self.moves[ch.square_name(square)])
            self.board.push(self.moves[ch.square_name(square)])
            self.play_state_sound()

            self.selected_piece = None
            self.selected_square = None
            self.moves.clear()

            self.draw_board(win)
            self.draw_pieces(win, pos)
            pygame.display.update()

            self.ai_move()

        self.selected_piece = None
        self.selected_square = None
        self.moves.clear()

        self.draw_board(win)
        self.draw_pieces(win, pos)
        pygame.display.update()

    def play_move_sound(self, move: chess.Move) -> None:
        """
        Play the move sound.
        """
        if self.board.is_capture(move) or self.board.is_en_passant(move):
            self.SOUNDS['capture'].play()
        elif self.board.is_castling(move):
            self.SOUNDS['castle'].play()
        else:
            self.SOUNDS['move'].play()

    def play_state_sound(self) -> None:
        """
        Play the game state sound.
        """
        if self.board.is_checkmate():
            self.SOUNDS['checkmate'].play()
        elif self.board.is_stalemate():
            self.SOUNDS['stalemate'].play()
        elif self.board.is_check():
            self.SOUNDS['check'].play()

    def ai_move(self) -> None:
        """
        Play the AI move.
        """
        self.human_turn = False
        possible_moves = [
            entry.move for entry in self.book.find_all(self.board)]
        if possible_moves:
            move = random.choice(possible_moves)
        else:
            move = self.MINIMAX.get_best_move(
                self.board, 20, False, 120)  # 2 minute cap
        self.play_move_sound(move)
        self.previous_squares = (move.from_square, move.to_square)
        self.board.push(move)
        self.play_state_sound()
        self.human_turn = True

    def quit(self) -> None:
        """
        Quit the Pygame window and game.
        """
        if self.board.is_game_over():
            pygame.quit()
