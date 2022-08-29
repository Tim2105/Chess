#imports
import pygame
import os
from pygame.locals import *
from Pieces import *
from Utiliti import *
from Draw import *

class Screen:
    def __init__(self):
        #initialize pygame
        pygame.display.init()
        #Screen erstellen
        screenWidth = 640
        screenHeight = 750
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        #Menü anzeigen
        self.menu_showed = False
        #Solange die Variable true ist soll das Spiel laufen
        self.running = True
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

    def start_game(self):

        self.board_X = 0
        self.board_Y = 0
        self.board_Width = (self.board_X, self.board_Y)

        board_src = os.path.join(self.sources, "board.png")
        self.board = pygame.image.load(board_src).convert()
        square_Length = self.board.get_rect().width // 8
        self.board_locations = []
        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append((self.board_X+(x*square_Length), self.board_Y+(y*square_Length)))

        pieces_src = os.path.join(self.sources, "figuren.png")
        self.pieces = pygame.image.load(pieces_src).convert()

        # initialize list that stores all places to put chess pieces on the board
        self.board_locations = []

        # calculate coordinates of the each square on the board
        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append([self.board_X+(x*square_Length), self.board_Y+(y*square_Length)])

        # get location of image containing the chess pieces
        pieces_src = os.path.join(self.sources, "figuren.png")
        # create class object that handles the gameplay logic
        self.draw = Draw(self.screen, pieces_src, self.board_locations, square_Length)

        # game loop
        while self.running:
            self.clock.tick(5)
            # poll events
            for event in pygame.event.get():
                # get keys pressed
                key_pressed = pygame.key.get_pressed()
                # check if the game has been closed by the user
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    # set flag to break out of the game loop
                    self.running = False
                elif key_pressed[K_SPACE]:
                    self.draw.reset()
            
            winner = self.draw.winner

            if self.menu_showed == False:
                self.show_menu()
            elif len(winner) > 0:
                self.ifWinner(winner)
            else:
                self.show_board()

            # for testing mechanics of the game
            #self.game()
            #self.declare_winner(winner)

            # update display
            pygame.display.flip()
            # update events
            pygame.event.pump()

        # call method to stop pygame
        pygame.quit()

    def show_menu(self):
        # background color
        bg_color = (139,69,19)
        # set background color
        self.screen.fill(bg_color)
        # black color
        black_color = (0, 0, 0)
        # coordinates for "Play" button
        start_Solo_btn = pygame.Rect(235, 300, 200, 50)
        start_Together_btn = pygame.Rect(235, 370, 200, 50)
        # show play button
        pygame.draw.rect(self.screen, black_color, start_Solo_btn)
        pygame.draw.rect(self.screen, black_color, start_Together_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont('comicsansms', 50)
        small_font = pygame.font.SysFont('Calibri', 20)
        # create text to be shown on the game menu
        welcome_text = big_font.render("Schach", False, black_color)
        created_by = small_font.render("Created by: Tim Plotzki und Nils Bachmann", True, black_color)
        start_Together_btn_label = small_font.render("Play Together", True, white_color)
        start_Solo_btn_label = small_font.render("Play Solo", True, white_color)
        
        # show welcome text
        self.screen.blit(welcome_text, ((self.screen.get_width() - welcome_text.get_width()) // 2, 150))
        # show credit text
        self.screen.blit(created_by, ((self.screen.get_width() - created_by.get_width()) // 2, self.screen.get_height() - created_by.get_height() - 100))
        # show text on the Play button
        self.screen.blit(start_Together_btn_label, ((start_Solo_btn.x + (start_Solo_btn.width - start_Together_btn_label.get_width()) // 2, start_Solo_btn.y + (start_Solo_btn.height - start_Together_btn_label.get_height()) // 2)))
        self.screen.blit(start_Solo_btn_label, ((start_Together_btn.x + (start_Together_btn.width - start_Solo_btn_label.get_width()) // 2, start_Together_btn.y + (start_Together_btn.height - start_Solo_btn_label.get_height()) // 2)))

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utiliti()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if start_Together_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, start_Together_btn, 3)
                self.menu_showed = True
            elif start_Solo_btn.collidepoint(mouse_coords[1], mouse_coords[2]):
                pygame.draw.rect(self.screen, white_color, start_Solo_btn, 3)
                self.menu_showed = True
            # check if enter or return key was pressed
            elif key_pressed[K_RETURN]:
                self.menu_showed = True

    def show_board(self):
        colour=(255, 255, 255)
        self.screen.fill(colour)
        self.screen.blit(self.board, self.board_Width)
        self.draw.play_turn()
        self.draw.draw_pieces()


    def ifWinner(self, winner):
        # background color
        bg_color = (255, 255, 255)
        # set background color
        self.screen.fill(bg_color)
        # black color
        black_color = (0, 0, 0)
        # coordinates for play again button
        reset_btn = pygame.Rect(250, 300, 140, 50)
        # show reset button
        pygame.draw.rect(self.screen, black_color, reset_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont('comicsansms', 50)
        small_font = pygame.font.SysFont('comicsansms', 20)

        # text to show winner
        text = winner + " wins!" 
        winner_text = big_font.render(text, False, black_color)

        # create text to be shown on the reset button
        reset_label = "Play Again"
        reset_btn_label = small_font.render(reset_label, True, white_color)

        # show winner text
        self.screen.blit(winner_text, ((self.screen.get_width() - winner_text.get_width()) // 2, 150))
        
        # show text on the reset button
        self.screen.blit(reset_btn_label, ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2, reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        utili = Utiliti()

        # check if left mouse button was clicked
        if utili.left_click_event():
            # call function to get mouse event
            mouse_coords = utili.get_mouse_event()

            # check if reset button was clicked
            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, reset_btn, 3)
                
                # change menu flag
                self.menu_showed = False
            # check if enter or return key was pressed
            elif key_pressed[K_RETURN]:
                self.menu_showed = False
            # reset game
            self.draw.reset()
            # clear winner
            self.draw.winner = ""