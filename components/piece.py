import pygame
from .constants import RED, SQUARE_SIZE, WHITE, CROWN


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, color: tuple, row: int, col: int) -> None:
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.king = False
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col*SQUARE_SIZE + SQUARE_SIZE//2
        self.y = self.row*SQUARE_SIZE + SQUARE_SIZE//2

    def draw(self, WIN):
        pygame.draw.circle(WIN, WHITE, (self.x, self.y),
                           SQUARE_SIZE//2-self.PADDING+self.OUTLINE)
        pygame.draw.circle(WIN, self.color, (self.x, self.y),
                           SQUARE_SIZE//2-self.PADDING)
        if self.king:
            WIN.blit(CROWN, (self.x-CROWN.get_width() //
                             2, self.y-CROWN.get_height()//2))

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
