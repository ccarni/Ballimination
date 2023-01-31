import random

import pygame

# this is a button
class Button:
    def __init__(self, text, rect, color):
        self.rect = rect
        font = pygame.font.Font(None, 100)
        bg_font = pygame.font.Font(None, 101)
        bg_text = bg_font.render(text, False, color_offset(color))
        text = font.render(text, False, color)
        surf = pygame.Surface(text.get_size())
        surf.fill((60, 86, 122))
        surf.blit(bg_text, (0, 0))
        surf.blit(text, (0, 0))
        self.surf = pygame.transform.scale(surf, rect.size)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        # this will make david laugh


def color_offset(color):
    new_color = [0, 0, 0]
    for i in range(3):
        new_color[i] = color[i] - 50
        if new_color[i] < 0:
            new_color[i] = 20
        if new_color[i] > 255:
            new_color[i] = 255
    return new_color