import pygame
from pygame.locals import *

from Pieces import Pieces
from Board import *
from ChessUtils import *


class Draw(object):
    def __init__(self, screen, pieces_src, square_length, board):
        self.board = board
        # display surface
        self.screen = screen
        self.board = board
        self.square_length = square_length
        self.pieces_src = pieces_src
        # create an object of class to show chess pieces on the board
        self.chess_pieces = Pieces(self.pieces_src, 6, 2, self.board)   

    def draw_turn(self):
        # white color
        white_color = (0, 0, 0)
        # create fonts for texts
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        if self.board.turn == 0:
            turn_text = small_font.render("Weiß ist am Zug", True, white_color)
        elif self.board.turn == 1:
            turn_text = small_font.render("Schwarz ist am Zug", True, white_color)
        
        # show welcome text
        self.screen.blit(turn_text, ((self.screen.get_width() - turn_text.get_width()) // 2, 10))

    # Methode für die Gamelogik
    def gamelogic_two_player(self):
        transparent_green = (0,194,39,170)
        transparent_blue = (28,21,212,170)

        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)
        for piece in self.board.pieces:
            self.chess_pieces.draw(self.screen, piece)
        pygame.display.flip()

        selected_Square_x, selected_Square_y = self.get_selected_square()
        move = None
        if self.board.board[selected_Square_x][selected_Square_y] != None and self.board.board[selected_Square_x][selected_Square_y].color == self.board.turn:
            self.legalMoves = self.board.get_legal_moves_from_pos((selected_Square_x, selected_Square_y))
            self.screen.blit(surface, (selected_Square_x*80, (7-selected_Square_y)*80+50))
            for legal in self.legalMoves:
                self.screen.blit(surface1, (legal.to[0]*80, (7-legal.to[1])*80+50))
            for piece in self.board.pieces:
                self.chess_pieces.draw(self.screen, piece)
            pygame.display.flip()
            
            move_to_square_x, move_to_square_y = self.get_selected_square()
            print(move_to_square_x, move_to_square_y)
            isBreak=True
            for possible_move in self.legalMoves:
                if isBreak:
                    if (selected_Square_x, selected_Square_y) == possible_move.fr and (move_to_square_x, move_to_square_y) == possible_move.to:
                        move = possible_move
                        print("sdfas")
                        if isinstance(self.board.board[selected_Square_x][selected_Square_y], Pawn):
                            print("sdasd")
                            if move_to_square_y == 0 or move_to_square_y == 7:
                                print("sdf")
                                promo = self.promotion()
                                for legal in self.legalMoves:
                                    if move.fr == legal.fr and isinstance(legal.promotion_piece, promo):
                                        move = legal
                                        isBreak = False
                                        break
                        if move != None:
                            print("moive")
                            self.board.do_move(move)
                            isBreak = False
                else:
                    break         
        for piece in self.board.pieces:
            self.chess_pieces.draw(self.screen, piece)
        pygame.display.flip()      

    def draw_computer(self):
        for piece in self.board.pieces:
            self.chess_pieces.draw(self.screen, piece)  
        pygame.display.flip()  

    def promotion(self):
        #Definition der Farben und Schriftart und Größe
        print("Promotion")
        background_color = (139,69,19)
        self.screen.fill(background_color)
        black_color = (0,0,0)
        white = (255,255,255)
        font = pygame.font.SysFont('comicsansms', 20)
        #Position der Button
        queen = pygame.Rect(220, 110, 200, 50)
        rook = pygame.Rect(220, 220, 200, 50)
        bishop = pygame.Rect(220, 330, 200, 50)
        knight = pygame.Rect(220, 440, 200, 50)
        #Initialisierung der Button
        pygame.draw.rect(self.screen, black_color, queen)
        pygame.draw.rect(self.screen, black_color, rook)
        pygame.draw.rect(self.screen, black_color, bishop)
        pygame.draw.rect(self.screen, black_color, knight)
        #Text auf dem Button
        queen_label = font.render("Dame", True, white)
        rook_label = font.render("Turm", True, white)
        bishop_label = font.render("Läufer", True, white)
        knight_label = font.render("Springer", True, white)
        #Position des Textes auf dem Button
        self.screen.blit(queen_label, (queen.x + (queen.width - queen_label.get_width()) // 2, queen.y + (queen.height - queen_label.get_height()) // 2))
        self.screen.blit(rook_label, (rook.x + (rook.width - rook_label.get_width()) // 2, rook.y + (rook.height - rook_label.get_height()) // 2))
        self.screen.blit(bishop_label, (bishop.x + (bishop.width - bishop_label.get_width()) // 2, bishop.y + (bishop.height - bishop_label.get_height()) // 2))
        self.screen.blit(knight_label, (knight.x + (knight.width - knight_label.get_width()) // 2, knight.y + (knight.height - knight_label.get_height()) // 2))
        pygame.display.flip()
        #Auswahl des Buttons
        while True:
            mouseposition = self.get_mouse_pos()
            if queen.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white, queen, 3)
                return Queen
            elif rook.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white, rook, 3)
                return Rook
            elif bishop.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white, bishop, 3)
                return Bishop
            elif knight.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white, knight, 3)
                return Knight
            
    #Methode zum bestimmen des Feldes eines Linksklicks
    def get_selected_square(self):
        pygame.event.clear()
        event = pygame.event.wait()
        while pygame.MOUSEBUTTONDOWN != event.type:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            event = pygame.event.wait()

        mousepos = pygame.mouse.get_pos()
        return (mousepos[0]//80, ((690 - mousepos[1])//80))

    def get_mouse_pos(self):
        pygame.event.clear()
        event = pygame.event.wait()
        while pygame.MOUSEBUTTONDOWN != event.type:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            event = pygame.event.wait()

        mousepos = pygame.mouse.get_pos()
        return mousepos