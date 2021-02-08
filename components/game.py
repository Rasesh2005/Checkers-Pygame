import pygame

from .constants import *
from .board import Board
from .piece import Piece

class Game:
    def __init__(self,win) -> None:
        self.selected=None
        self.board=Board()
        self.turn=RED
        self.valid_moves={}
        self.WIN=win

    def update(self):
        self.board.draw(self.WIN)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    def reset(self):
        self.selected=None
        self.board=Board()
        self.turn=RED
        self.valid_moves={}
    def select(self,row,col):
        if self.selected:
            temp=self.selected
            result=self.__move(row,col)
            if not result:
                self.selected=temp
        piece=self.board.get_board_piece(row,col)
        if piece!=0 and piece.color==self.turn:
            self.selected=piece
            self.valid_moves=self.board.get_valid_moves(piece)
            print(self.valid_moves)
            print("Selected ",row,col)
            return True

    def draw_valid_moves(self,moves:dict):
        for move in moves:
            row,col=move
            pygame.draw.circle(self.WIN,BLUE,(col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2),15)

    def winner(self):
        winner=None
        if not self.board.red_pieces_left or not self.movesLeft(RED):
            winner="WHITE"
        if not self.board.white_pieces_left or not self.movesLeft(WHITE):
            winner="RED"

        return winner
    def movesLeft(self,color):
        for row in self.board.board:
            for piece in row:
                if piece!=0 and piece.color==color and len(self.board.get_valid_moves(piece)):
                    return True
        return False
    def __move(self,row,col):
        piece=self.board.get_board_piece(row,col)
        if piece==0 and self.selected and (row,col) in self.valid_moves:
            self.board.move_piece(self.selected,row,col)
            self.change_turn()
            skipped=self.valid_moves.get((row,col))
            self.valid_moves={}
            print("Skipped Coin at: ",skipped)
            if skipped:
                self.board.remove(skipped)
        else:
            return False
        return True
    
    def change_turn(self):
        if self.turn==RED:
            self.turn=WHITE
        else:
            self.turn=RED

