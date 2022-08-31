import os
import pygame
from ChessUtils import *
from Board import *
from Screen import *
#Zeichnen einzelner Figuren
class Pieces(pygame.sprite.Sprite):
    #Initialisieren
    def __init__(self, filename, cols, rows, board):
        self.board = board
        pygame.sprite.Sprite.__init__(self)
        self.index = {
            King: 0,
            Queen: 1,
            Bishop: 2,
            Knight: 3,
            Rook: 4,
            Pawn: 5
        }
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows

        self.cells = list([(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)])

    #Zeichnen einer Figur
    def draw(self, screen, piece):
        self.piece_index = self.index[type(piece)] + 6 * (piece.color)
        x, y = piece.pos
        x = x * 80
        y = 690 - (y + 1)* 80
        screen.blit(self.spritesheet, (x, y), self.cells[self.piece_index])