import pygame
from pygame.math import Vector2
import random
import numpy as np
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, runner, pos=(0, 0), v=(0,0)):


        # Set runner
        self.runner = runner     

        # Set Colors
        self.normal_color = (color[0] - 40, color[1] - 40, color[2] - 40)
        self.flying_color = (100, 255, 100)
        self.ground_color = (100, 100, 100)
        self.color = self.normal_color


        # SPRITE STUFF
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pygame.surface.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        pygame.draw.ellipse(self.image, (255, 255, 255), self.image.get_rect())
        pygame.draw.ellipse(self.image, color, self.image.get_rect(), width=int(radius*0.5)) 
        self.image.set_colorkey((0,0,0))

        # Our game :D
        self.flying = False
        self.throw_speed = 7
        self.throw_speed /= 10 # So that the tick that makes it consistent across framerates doesn't make it go waaaay too fast
        self.player = None

        # Flying Timer
        self.flying_timer = 0
        self.max_flying_timer = 2000

        # Get Rekt
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # Physics Shenanigans
        self.mass = math.pi*radius*radius


        # Velocity
        self.v = np.array([0.0, 0.0], dtype='float64')

    def update_sprite(self):
        radius = self.radius
        color = self.color
        self.image = pygame.surface.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        pygame.draw.ellipse(self.image, (255, 255, 255), self.image.get_rect())
        pygame.draw.ellipse(self.image, color, self.image.get_rect(), width=int(radius*0.5)) 
        self.image.set_colorkey((0,0,0))

    def update(self, bounds):

        # Flying Timer
        if self.flying_timer > 0:
            self.flying_timer -= 1 * self.runner.tick
        if self.flying_timer <= 0 and self.flying == True:
            # Stop flying
            self.flying = False
            self.normal_color = self.ground_color

        if self.flying_timer < self.max_flying_timer / 1.5:
            self.v *= 0.95

        # Stop if on ground
        if self.flying == False:
            self.v = np.array([0.0, 0.0], dtype='float64')

        # Update Position
        self.rect.x += float(self.v[0] * self.throw_speed * self.runner.tick)
        self.rect.y += float(self.v[1] * self.throw_speed * self.runner.tick)

        if self.flying:
            self.color = self.flying_color
        if not self.flying:
            self.color = self.normal_color

        # Dont go through walls, walls exist >:(
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.v[0] *= -1.0
        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.v[1] *= -1.0
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.v[0] *= -1.0
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.v[1] *= -1.0

        # Update the color
        self.update_sprite()

    def draw(self, screen):
        screen.blit(self.image, self.rect)