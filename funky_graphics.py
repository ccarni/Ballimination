import pygame
import numpy as i_will_not_use_this # for the lols
import random

def do_rotate(surf, dir):
    left = -90
    right = 90
    surface = surf
    if dir == [0, 1]:
        surface = pygame.transform.rotate(surf, left)
    if dir == [0, -1]:
        surface = pygame.transform.rotate(surf, right)
    if dir == [-1, 0]:
        surface = pygame.transform.rotate(surf, right * 2)
    if dir == [1, 0]:
        pass  # Already looking this way
    return surface

def draw_player(head_radius, color, pos, screen, rotation_dir):
    #head_radius = head_radius / 5
    
    def hr(x=1.0):
        return head_radius * x
    
    player_surf = pygame.surface.Surface((head_radius * 3.5, head_radius * 5))
    player_surf.fill((0, 0, 0, 0))
    player_head = pygame.rect.Rect(hr(0.5), hr(1.5), hr(2), hr(2))
    player_body = pygame.rect.Rect(hr(), hr(0.65), hr(), hr(3.75))
    ear_width = 0.6
    ear_height = 0.3
    player_l_ear = pygame.rect.Rect(hr(1.2), hr(1.2), hr(ear_width), hr(ear_height))
    player_r_ear = pygame.rect.Rect(hr(1.2), hr(3.5), hr(ear_width), hr(ear_height))
    hand_radius = 0.5
    player_l_hand = pygame.rect.Rect(hr(3), hr(0.45), hr(hand_radius), hr(hand_radius))
    player_r_hand = pygame.rect.Rect(hr(3), hr(4.2), hr(hand_radius), hr(hand_radius))
    # when you change player radius, change last value
    body_color = (114, 114, 114)
    pygame.draw.line(player_surf, body_color, (hr(3.5), hr(0.65)), (hr(), hr(0.65)), 5)
    pygame.draw.line(player_surf, body_color, (hr(3), hr(4.4)), (hr(), hr(4.4)), 5)
    pygame.draw.rect(player_surf, color, player_l_hand)
    pygame.draw.rect(player_surf, color, player_r_hand)
    pygame.draw.rect(player_surf, color, player_body)
    ear_color = (85, 85, 85)
    pygame.draw.rect(player_surf, ear_color, player_l_ear)
    pygame.draw.rect(player_surf, ear_color, player_r_ear)
    eye_color = (255, 236, 143)
    pygame.draw.circle(player_surf, eye_color, (hr(2.35), hr(2)), hr(0.3))
    pygame.draw.circle(player_surf, eye_color, (hr(2.35), hr(3)), hr(0.3))
    pygame.draw.rect(player_surf, body_color, player_head)
    player_surf.set_colorkey((0, 0, 0))
    player_surf = do_rotate(player_surf, rotation_dir)
    #return player_surf
    screen.blit(player_surf, pos)


#COW TOOLS
def clip(number, lower, upper):
    number = max(lower, number)
    number = min(upper, number)
    return number

# This updates the color of a pixel by amount
def update_color(surf, point, amount):
    color = surf.get_at(point)
    color[0] = clip(color[0] + amount[0], 0, 255)
    color[1] = clip(color[1] + amount[1], 0, 255)
    color[2] = clip(color[2] + amount[2], 0, 255)
    surf.set_at(point, color)

# This helps smooth over random noise to (hopefully) improve quality of the images
def update_surrounding(surf, i, j, amount):
    update_color(surf, (i, j), amount)

    amount2 = [amount[i] // 1 for i in range(3)]
    right = ((i + 1) % surf.get_width(), j)
    left = ((i - 1 + surf.get_width()) % surf.get_width(), j)
    up = (i, (j - 1 + surf.get_height()) % surf.get_height())
    down = (i, (j + 1) % surf.get_height())
    update_color(surf, right, amount2)
    update_color(surf, left, amount2)
    update_color(surf, up, amount2)
    update_color(surf, down, amount2)
    
####IMPORTANT STUFF THAT DOES THE THING
def screener(screen, back_color = (200, 191, 157)):
    surf = pygame.Surface((screen.get_width()/25, screen.get_height()/25))
    surf.fill(back_color)
    for i in range(surf.get_width()):
        for j in range(surf.get_height()):
            amount = [random.randint(-3, 3) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    surf = pygame.transform.scale(surf, (screen.get_width(), screen.get_height()))        
    return surf




def background(scree, scr):
    # SCREEEEEEEEEE
    ###THE PART THAT DOES
    scree.blit(scr, (0, 0))#IMP# end of refactored graphics codeO



def draw_winning_robot(screen, color):
    norm_color = (114, 114, 114)
    win_surf = pygame.surface.Surface((screen.get_width()*.5, screen.get_height()*.5 ))
    win_surf.fill((0,0,0,0))
    win_body = pygame.rect.Rect((screen.get_width()* 0.1, screen.get_height()*0.3), (screen.get_width()*0.1, screen.get_height()* 0.2))
    win_head = pygame.rect.Rect((screen.get_width()* 0.112, screen.get_height()*0.18), (screen.get_width()*0.075, screen.get_height()* 0.13))
    win_l_arm = pygame.rect.Rect((screen.get_width()* 0.09, screen.get_height()*0.08), (screen.get_width()*0.01, screen.get_height()* 0.3))
    win_r_arm = pygame.rect.Rect((screen.get_width()* 0.199, screen.get_height()*0.08), (screen.get_width()*0.01, screen.get_height()* 0.3))
    win_r_hand = pygame.rect.Rect((screen.get_width()* 0.079, screen.get_height()*0.07), (screen.get_width()*0.03, screen.get_width()*0.03))
    win_l_hand = pygame.rect.Rect((screen.get_width()* 0.19, screen.get_height()*0.07), (screen.get_width()*0.03, screen.get_width()*0.03))
    pygame.draw.rect(win_surf, norm_color, win_head)
    pygame.draw.circle(win_surf, (255, 236, 143), (screen.get_width()* 0.132, screen.get_height()*0.22), screen.get_height() *0.017)
    pygame.draw.circle(win_surf, (255, 236, 143), (screen.get_width()* 0.172, screen.get_height()*0.22), screen.get_height() *0.017)
    pygame.draw.rect(win_surf, norm_color, win_r_arm)
    pygame.draw.rect(win_surf, norm_color, win_l_arm)
    pygame.draw.rect(win_surf, color, win_body)
    pygame.draw.rect(win_surf, color, win_r_hand)
    pygame.draw.rect(win_surf, color, win_l_hand)
    screen.blit(win_surf, (0, 0))
