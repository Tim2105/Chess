#imports
import pygame
import os
from pygame.locals import *
from ChessComputer import ChessComputer
from Pieces import *
from Draw import *

class Screen:
    def __init__(self):
        #Initialisiere pygame und das Board Objekt
        self.board = Board()
        pygame.display.init()
        #Screen erstellen
        self.screenWidth = 640
        self.screenHeight = 690
        self.square_Length = 80
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        #Menü anzeigen
        self.menu_showed = False
        #Solange die Variable true ist soll das Spiel laufen
        self.running = True
        self.Solo = False
        #Rescourcen laden
        self.sources = "res" 
        #Bildschirm Aktualisierungsrate
        self.clock = pygame.time.Clock()
        #Titel und Icon setzen
        pygame.display.set_caption("Schach")
        icon_src = os.path.join(self.sources, "icon.png")
        icon = pygame.image.load(icon_src)
        pygame.display.set_icon(icon)
        pygame.display.flip()
        self.clock = pygame.time.Clock()

    #Spiel Schleife
    def start_game(self):
        self.board_X = 0
        self.board_Y = 50
        self.board_Width = (self.board_X, self.board_Y)
        board_src = os.path.join(self.sources, "board.png")
        self.boardLoad = pygame.image.load(board_src).convert()
        
        self.pieces_src = os.path.join(self.sources, "figuren.png")
        self.pieces_con = pygame.image.load(self.pieces_src).convert()

        self.draw = Draw(self.screen, self.pieces_src, self.square_Length, self.board)

        #Schleife die solange ausführt wie das Programm laufen soll
        while self.running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if self.menu_showed == False:
                pygame.display.flip()
                self.show_menu()
            elif self.get_winner(): 
                self.wennWinner()
            elif self.Solo == True:
                self.solo_game()
            else:
                self.two_player()

            pygame.display.flip()
            pygame.event.pump()

        pygame.quit()

    #Menü anzeigen
    def show_menu(self):
        background_color = (139,69,19)
        self.screen.fill(background_color)
        black_color = (0, 0, 0)
        white_color = (255, 255, 255)
        #Koordinaten der Button
        start_Solo_btn = pygame.Rect(220, 300, 200, 50)
        start_Together_btn = pygame.Rect(220, 370, 200, 50)
        #Initialisieren der Button
        pygame.draw.rect(self.screen, black_color, start_Solo_btn)
        pygame.draw.rect(self.screen, black_color, start_Together_btn)      
        #Schriftart die verwendet werden soll
        big_font = pygame.font.SysFont('comicsansms', 50)
        small_font = pygame.font.SysFont('Calibri', 20)
        #Text der angezeigt werden soll
        headline = big_font.render("Schach", False, black_color)
        created_by = small_font.render("Created by: Tim Plotzki und Nils Bachmann", True, black_color)
        #Rendern der Button
        start_Together_btn_label = small_font.render("Play Together", True, white_color)
        start_Solo_btn_label = small_font.render("Play Solo", True, white_color)
        #Koordinaten für Button und Text
        start_Together_btn_label_x = start_Together_btn.x + (start_Together_btn.width - start_Together_btn_label.get_width()) // 2
        start_Together_btn_label_y = start_Together_btn.y + (start_Together_btn.height - start_Together_btn_label.get_height()) // 2

        start_Solo_btn_label_x = start_Solo_btn.x + (start_Solo_btn.width - start_Solo_btn_label.get_width()) // 2
        start_Solo_btn_label_y = start_Solo_btn.y + (start_Solo_btn.height - start_Solo_btn_label.get_height()) // 2

        headline_x = (self.screen.get_width() - headline.get_width()) // 2
        headline_y = 150

        created_by_x = (self.screen.get_width() - created_by.get_width()) // 2
        created_by_y = self.screen.get_height() - created_by.get_height() - 100


        #Überschrift anzeigen
        self.screen.blit(headline, (headline_x, headline_y))
        #Created by anzeigen
        self.screen.blit(created_by, (created_by_x, created_by_y))
        #Button anzeigen
        self.screen.blit(start_Solo_btn_label, (start_Solo_btn_label_x, start_Solo_btn_label_y))
        self.screen.blit(start_Together_btn_label, (start_Together_btn_label_x, start_Together_btn_label_y))
        pygame.display.flip()
        while self.menu_showed == False:
            mouseposition = self.get_mouse_pos()
            if start_Solo_btn.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white_color, start_Solo_btn, 3)
                self.Solo = True
                self.menu_showed = True
            elif start_Together_btn.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white_color, start_Together_btn, 3)
                self.menu_showed = True
            pygame.display.flip()

    #Bestimmen ob es einen Gewinner gibt
    def get_winner(self) -> bool:
        if len(self.board.get_legal_moves(self.board.turn)) == 0 and self.board.is_in_check(self.board.turn):
            print("ad")
            return True
    #Zwei Spieler spielen aufruf der Funktionen die benötigt werden
    def two_player(self):
        color = (155, 155, 155)
        self.screen.fill(color)
        self.screen.blit(self.boardLoad, self.board_Width)
        self.draw.draw_turn()
        self.draw.gamelogic_two_player()

    #Solo Spieler spielen aufruf der Funktionen die benötigt werden
    def solo_game(self):
        color = (155, 155, 155)
        self.screen.fill(color)
        self.screen.blit(self.boardLoad, self.board_Width)
        self.draw.draw_turn()
        self.draw.gamelogic_two_player()
        pygame.display.flip()
        if self.board.turn == 1:
            self.computer()

    #Computer spielt, 
    def computer(self):
        chesscomputer = ChessComputer()
        chesscomputermove = chesscomputer.get_move(self.board)
        if chesscomputermove == None:
            return
        self.board.do_move(chesscomputermove)
        self.draw.draw_computer()

    #Wenn es einen Gewinner gibt, wird dieser angezeigt
    def wennWinner(self):
        #Hintergrundfarbe und Schriftart
        background_color = (155, 155, 155)
        self.screen.fill(background_color)
        black_color = (0, 0, 0)
        white_color = (255, 255, 255)
        reset_btn = pygame.Rect(245, 300, 140, 50)
        pygame.draw.rect(self.screen, black_color, reset_btn)        
        big_font = pygame.font.SysFont('comicsansms', 50)
        small_font = pygame.font.SysFont('comicsansms', 20)
        #Text der angezeigt werden soll wer gewonnen hat
        if self.board.turn == 1:
            text = "Weiß hat gewonnen!"
        else:
            text = "Schwarz hat gewonnen!"
        #Text anzeigen und Button anzeigen
        winner_text = big_font.render(text, False, black_color)
        reset_label = "Menü"
        reset_btn_label = small_font.render(reset_label, True, white_color)
        self.screen.blit(winner_text, ((self.screen.get_width() - winner_text.get_width()) // 2, 150))        
        self.screen.blit(reset_btn_label, ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2, reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))
        pygame.display.flip()
        #Wenn der Reset Button geklickt wird, wird das Spiel neugestartet
        while self.menu_showed == True:
            mouseposition = self.get_mouse_pos()
            if reset_btn.collidepoint(mouseposition):
                pygame.draw.rect(self.screen, white_color, reset_btn, 3)
                self.menu_showed = False
                self.board = Board()
                self.draw = Draw(self.screen, self.pieces_src, self.square_Length, self.board)
                pygame.display.flip()

    #Bestimmen der Mauskoordinaten
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