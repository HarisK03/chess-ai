import pygame
from constants import WIDTH, HEIGHT, FPS
from board import Board

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
board = Board()


def main() -> None:
    """
    The main function. Start the pygame window and the game.
    """
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.select_square(pygame.mouse.get_pos(), True)
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.event.set_grab(False)
                board.release_square(pygame.mouse.get_pos(), WIN)

            if pygame.mouse.get_pressed()[0]:
                pygame.event.set_grab(True)
                try:
                    board.select_square(pygame.mouse.get_pos(), False)
                except AttributeError:
                    pass

        board.draw_board(WIN)
        board.draw_pieces(WIN, pygame.mouse.get_pos())
        pygame.display.update()

        board.quit()

    pygame.quit()


if __name__ == "__main__":
    main()
