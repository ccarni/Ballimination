import pygame
import random
import sys
import numpy as np
import math
import input_handler
from player import Player
from ball import Ball
import funky_graphics
import button
import physics


class Runner():
    def __init__(self, players):
        self.screen = pygame.display.set_mode()
        self.background_color = (0, 50, 0)
        self.balls = pygame.sprite.Group()

        # Trails? Maybe?
        self.alpha_surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        self.scr = funky_graphics.screener(self.screen, self.background_color)

        # The input handler
        self.input_boi = input_handler.Input_Handler()

        # World stuff
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # Player spawn parameters
        distance_from_edge = 100
        balls_distance_from_edge = 100

        # Create players
        player_size = 25
        self.player1 = Player(player_size, player_size, self, 5)
        self.player2 = Player(player_size, player_size, self, 5, (200, 50, 50), [pygame.K_t, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_v, pygame.K_n]) 
        self.player3 = Player(player_size, player_size, self, 5, (80, 80, 255), [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_PERIOD])
        self.player4 = Player(player_size, player_size, self, 5, (200, 200, 50), [pygame.K_KP_8, pygame.K_KP_4, pygame.K_KP_5, pygame.K_KP_6, pygame.K_KP_1, pygame.K_KP_3])
        self.player1.pos = [distance_from_edge, distance_from_edge]
        self.player2.pos = [self.screen_width - distance_from_edge, distance_from_edge]
        self.player3.pos = [distance_from_edge, self.screen_height - distance_from_edge]
        self.player4.pos = [self.screen_width - distance_from_edge, self.screen_height - distance_from_edge]

        self.players = pygame.sprite.Group()
        if players[3]:
            self.players.add(self.player4)
        if players[2]:
            self.players.add(self.player3)
        if players[1]:
            self.players.add(self.player2)
        if players[0]:
            self.players.add(self.player1)


        # Min/max ball count
        self.min_balls = 3
        self.max_balls = 9

        # Create Balls
        ball_count = random.randint(self.min_balls,self.max_balls)
        for i in range(ball_count):
            rx = random.randint(balls_distance_from_edge, self.screen_width - balls_distance_from_edge)
            ry = random.randint(balls_distance_from_edge, self.screen_height - balls_distance_from_edge)
            ball1 = Ball((50, 50, 50), 10, self, [rx, ry], [0, 0])
            
            self.balls.add(ball1)

        # Tick for accurate timescale
        self.tick = 0
        # Clock for checking how much time we have left to program this thing
        self.clock = pygame.time.Clock()
        # zoom
        self.FPS = 60

        # Win stuff
        self.winning_color = (0, 0, 0)
        self.won = False

        self.reset_players = players

    def update(self):
        # Tick clock
        self.tick = self.clock.tick(self.FPS)

        # Balls  Trailstrails snails cails
        self.alpha_surf.fill((255, 255, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)


        
        # Do input
        events = pygame.event.get()
        for event in events:
            self.input_boi.do_input(event, self.players)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.won:
                    self.__init__(self.reset_players)

        # Update all players
        downed = 0
        for player in self.players:
            player.update(events, bounds=self.screen.get_rect())
            if player.down:
                downed += 1

        if downed >= len(list(self.players)) - 1:
            for player in self.players:
                if not player.down:
                    self.win(player)
                    self.won = True
            
        # Update all balls
        for ball in self.balls:
            ball.update(bounds=self.screen.get_rect())
        
        # Do collisions
        collided = pygame.sprite.groupcollide(self.balls, self.players, False, False, self.ball_player_collision)
        ballboing = pygame.sprite.groupcollide(self.balls, self.balls, False, False, self.ball_player_collision)

        for ball in collided.keys():
            for plr in collided[ball]:
                plr.collide_with_ball(ball)

        for ball1 in ballboing.keys():
            for ball2 in ballboing[ball1]:
                physics.elastic_collision(ball1, ball2)
                ballboing[ball2].remove(ball1)



        # # WIN SHENANIGANS
        # downed = []
        # for player in self.players:
        #     if player.down:
        #         downed.append(player)

        # if len(downed) >= len(list(self.players)) - 1:
        #     for player in self.players:
        #         if not player.down:
        #             self.win(player)



    def win(self, player):
        self.winning_color = player.color
        self.won = True
        #print("This player won!!! YAY: " + str(player))
        

    def draw(self):
        # Reset background
        funky_graphics.background(self.screen, self.scr)

        # Draw all players
        for player in self.players:
            player.draw(self.screen)

        # the balls are now on the surfing board zooomb
        self.balls.draw(self.alpha_surf)
        # yeyeyeye alpha surf go brr onto scren yes
        self.screen.blit(self.alpha_surf, (0, 0))


        # Draw all balls
        for ball in self.balls:
            ball.draw(self.screen)


        if self.won:
            funky_graphics.draw_winning_robot(self.screen, self.winning_color)
        

        # Remember this thing future me |
        #                               v
        pygame.display.update()

        

    def ball_player_collision(self, ball1, ball2):
        if ball1 == ball2:
            return False
        r1 = ball1.rect.width/2
        r2 = ball2.rect.width/2

        x1, y1 = ball1.rect.center
        x2, y2 = ball2.rect.center

        if math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < r1 + r2:
            return True
        return False