import pygame
import sys

class Input_Handler():
    def __init__(self):
        self.left_click = False
        self.right_click = False
        self.middle_click = False



    def key_down(self, event, key):
        if event.type == pygame.KEYDOWN:
            if event.key == key:
                return True
            return False

    def key_up(self, event, key):
        if event.type == pygame.KEYUP:
            if event.key == key:
                return True
            return False

    def do_input(self, event, players):
        for player in players:
            c_index = 0
            for control in player.controls:
                state = None
                if self.key_down(event, control):
                    state = True
                if self.key_up(event, control):
                    state = False
                player.update_controls(c_index, state)
                c_index += 1


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click = True
            if event.button == 2:
                self.middle_click = True
            if event.button == 3:
                self.right_click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_click = False
            if event.button == 2:
                self.middle_click = False
            if event.button == 3:
                self.right_click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()