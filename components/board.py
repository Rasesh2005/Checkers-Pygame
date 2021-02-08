from components.piece import Piece
import pygame
from .constants import HEIGHT, RED, BLACK, ROWS, COLS, SQUARE_SIZE, WHITE, WIDTH


class Board:
    def __init__(self) -> None:
        self.board = []
        self.create_board()
        self.red_pieces_left = self.white_pieces_left = 12
        self.red_kings = self.white_kings = 0

    def create_board(self):
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                if c % 2 != r % 2:
                    if r < 3:
                        row.append(Piece(WHITE, r, c))
                    elif r > 4:
                        row.append(Piece(RED, r, c))
                    else:
                        row.append(0)
                else:
                    row.append(0)
            self.board.append(row)

    def get_valid_moves(self, piece: Piece):
        moves = {}
        # a dictionary with move as key and killed piece if any on jumping over
        row, col = piece.row, piece.col
        left = col-1
        right = col+1
        if piece.king:
            moves.update(self.__traverse_left(row-1, max(row-3, -1), -1, piece.color, left,isKing=True))
            moves.update(self.__traverse_right(row-1, max(row-3, -1), -1, piece.color, right,isKing=True))
            moves.update(self.__traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left,isKing=True))
            moves.update(self.__traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right,isKing=True))
        elif  piece.color == RED:
            moves.update(self.__traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.__traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        elif piece.color == WHITE:
            moves.update(self.__traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self.__traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def __traverse_left(self, start, stop, step, color, left, skipped=[],isKing=False):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last+skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.__traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self.__traverse_right(r+step, row, step, color, left+1,skipped=last))
                    if isKing:
                        moves.update(self.__traverse_left(r+step, row, step, color, left-1,skipped=last))
                        moves.update(self.__traverse_right(r+step, row, step, color, left+1,skipped=last))
                
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def __traverse_right(self, start, stop, step, color, right, skipped=[],isKing=False):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last+skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.__traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self.__traverse_right(r+step, row, step, color, right+1,skipped=last))
                    if isKing:
                        moves.update(self.__traverse_left(r+step, row, step, color, right-1,skipped=last))
                        moves.update(self.__traverse_right(r+step, row, step, color, right+1,skipped=last))
                    
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1

        return moves

    def remove(self,pieces:list):
        for piece in pieces:
            if piece.color==RED:
                self.red_pieces_left-=1
                print("1 Red piece Killed, Red pieces left: ",self.red_pieces_left)
            else:
                self.white_pieces_left-=1
                print("1 White piece Killed, White pieces left: ",self.white_pieces_left)
            self.board[piece.row][piece.col]=0

    def move_piece(self, piece: Piece, row, col):
        assert self.board[row][col] == 0
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS-1 or row == 0:
            # Make king when a move causes the piece to reach the other side
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_board_piece(self, row, col):
        return self.board[row][col]

    def draw_squares(self, WIN):
        WIN.fill(BLACK)
        for r in range(ROWS):
            for c in range(r % 2, COLS, 2):
                pygame.draw.rect(
                    WIN, RED, (r*SQUARE_SIZE, c*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, WIN):
        self.draw_squares(WIN)
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece != 0:
                    piece.draw(WIN)
