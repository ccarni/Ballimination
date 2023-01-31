import pygame
import random
import sys
from runner import Runner
import button

# The chance character : ◘


pygame.init()
screen = pygame.display.set_mode()  # lol no fullscreen?

players = [False, False, False, False]
player_keys = [pygame.K_z, pygame.K_v, pygame.K_m, pygame.K_KP1, pygame.K_1]
buttonstart = button.Button('start', pygame.Rect(screen.get_width() * 0.4, screen.get_height() * 0.7, screen.get_width() * 0.2, screen.get_height() * 0.2), (0, 0, 0))
buttontitle = button.Button('BALLIMINATION',
                            pygame.Rect(screen.get_width() * 0, screen.get_height() * 0, screen.get_width() * 0.9,
                                        screen.get_height() * 0.2), (255, 255, 255))
buttonp1 = button.Button('Player one: WASD to move, Z to pickup and spawn, C to throw', pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.2, screen.get_width() * 0.9, screen.get_height() * 0.05), (0, 0, 0))
buttonp2 = button.Button('Player two: TFGH to move, V to pickup and spawn, N to throw', pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.3, screen.get_width() * 0.9,
                                     screen.get_height() * 0.05), (0, 0, 0))
buttonp3 = button.Button('Player three: IJKL to move, M to pickup and spawn, . to throw',
                         pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.4, screen.get_width() * 0.9,
                                     screen.get_height() * 0.05), (0, 0, 0))
buttonp4 = button.Button('Player four: 8456 to move, 1 to pickup and spawn, 3 to throw ',
                         pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.5, screen.get_width() * 0.9,
                                     screen.get_height() * 0.05), (0, 0, 0))
button_how_start = button.Button('At least 2 players must be spawned to start',
                                 pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.6,
                                             screen.get_width() * 0.9, screen.get_height() * 0.05), (255, 255, 255))

buttonextra = button.Button('To move with p4, use a numpad',
                            pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.9, screen.get_width() * 0.5,
                                        screen.get_height() * 0.04), (255, 255, 255))

buttons = [buttonstart]
display_buttons = [buttontitle, buttonp1, buttonp2, buttonp3, buttonp4, button_how_start, buttonextra]

Continue_Loop = True

while Continue_Loop:
    mouse_loc = pygame.mouse.get_pos()
    active_button = None
    for the_button in buttons:
        if the_button.rect.collidepoint(mouse_loc):
            active_button = the_button

    

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if active_button is not None:
                    if sum(players) >= 2:
                        Continue_Loop = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                for i in range(5):
                    if event.key == player_keys[i]:
                        if i != 4:
                            players[i] = True
                        else:
                            players[3] = True
                        if i == 0:
                            buttonp1.__init__('Player one: WASD to move, Z to pickup and spawn, C to throw',
                                              pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.2,
                                                          screen.get_width() * 0.9, screen.get_height() * 0.05),
                                              (0, 255, 0))
                        if i == 1:
                            buttonp2.__init__('Player two: TFGH to move, V to pickup and spawn, N to throw',
                                              pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.3,
                                                          screen.get_width() * 0.9, screen.get_height() * 0.05),
                                              (255, 0, 0))
                        if i == 2:
                            buttonp3.__init__('Player three: IJKL to move, M to pickup and spawn, . to throw',
                                              pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.4,
                                                          screen.get_width() * 0.9, screen.get_height() * 0.05),
                                              (0, 0, 255))
                        if i == 3 or i == 4:
                            buttonp4.__init__('Player four: 8456 to move, 1 to pickup and spawn, 3 to throw ',
                                              pygame.Rect(screen.get_width() * 0, screen.get_height() * 0.5,
                                                          screen.get_width() * 0.9, screen.get_height() * 0.05),
                                              (255, 255, 0))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if active_button is not None:
                    if sum(players) >= 2:
                        Continue_Loop = False

    if sum(players) >= 2:
        buttonstart.__init__('start',
                             pygame.Rect(screen.get_width() * 0.4, screen.get_height() * 0.7, screen.get_width() * 0.2,
                                         screen.get_height() * 0.2), (255, 255, 255))
    screen.fill((60, 86, 122))
    for b in buttons:
        b.draw(screen)
    for b in display_buttons:
        b.draw(screen)
    pygame.display.update()

runner = Runner(players)

while True:
    runner.update()
    runner.draw()
