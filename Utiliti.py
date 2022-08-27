import pygame
import queue

class Utiliti:
    def get_mouse_event(self):
        # bestimmen der Mausposition
        position = pygame.mouse.get_pos()

        # gibt den Linksklickstatus und die Mausposition zurück
        return position

    def left_click_event(self):
        # speichert den Linksklickstatus
        mouse_btn = pygame.mouse.get_pressed()
        left_click = False

        if mouse_btn[0]:
            left_click = True

        return left_click 