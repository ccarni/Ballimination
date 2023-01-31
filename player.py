import pygame
import funky_graphics
import numpy as np
import input_handler

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, runner, move_speed = 5, color = (50, 200, 50), controls = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_z, pygame.K_c]):
        pygame.sprite.Sprite.__init__(self)
        
        self.controls = controls
        self.control_status = [False, False, False, False, False, False]
        self.pickup_control = False

        

        # Game-related Variables
        self.down = False
        self.move_speed = move_speed * 0.05
        self.runner = runner
        self.has_ball = False
        self.ball = None

        self.watching_player = None

        # Transform
        self.width = width
        self.height = height
        self.pos = [0, 0]

        # Overall ending direction
        self.direction = [0, 0]
        self.look_direction = [0, 0]

        # Surface
        self.surface = pygame.Surface((self.width, self.height))
        self.og_sprite = False

        # Set Rect
        self.rect = self.surface.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Color
        self.normal_color = color
        self.down_color = (int(color[0] * 0.5), int(color[1] * 0.5), int(color[2] * 0.5))
        self.color = self.normal_color

        # Add texture
        self.update_texture()
        self.surface = self.surface.convert()
        self.image = self.surface

    def update_texture(self):
        
        
        # Reset Rect
        self.rect = self.surface.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.og_sprite:
            self.surface.fill(self.color)
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0, 0, self.width, self.height), 2)
        

    def collide_with_ball(self, ball):

        if ball.flying == True:
            if ball.flying_color != self.color and not self.down:
                self.down = True
                # ADD STUFF FOR UN-ELIMINATION IF BALL's THROWER IS DOWN
                ball.flying = False
                ball.normal_color = ball.ground_color
                self.watching_player = ball.player
        else:
            # Pick Up
            if not self.has_ball and not self.down:
                if self.control_status[4]:
                    self.ball = ball
                    self.ball.normal_color = self.normal_color
                    self.ball.flying_color = self.normal_color
                    self.ball.color = self.normal_color
                    self.has_ball = True
                    self.ball.player = self
                    ball.kill()
                    del ball


    def update(self, events, bounds):
        # Reset direct
        self.direction = [0, 0]

        # Up
        if self.control_status[0]:
            self.direction[1] -= 1
        # Left
        if self.control_status[1]:
            self.direction[0] -= 1
        # Down
        if self.control_status[2]:
            self.direction[1] += 1
            
        # Right
        if self.control_status[3]:
            self.direction[0] += 1



        # Throw
        if self.control_status[4]: # only if "drop" is held down
            
            for event in events: # inneficient but works, change later
                if event.type == pygame.KEYDOWN:
                    if event.key == self.controls[4]:
                        self.throw(0)
        
        if self.control_status[5]:
            self.throw(1)


        # Dont go through walls, walls exist >:(
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            if self.direction[0] == -1:
                self.direction[0] = 0
        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            if self.direction[1] == -1:
                self.direction[1] = 0
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            if self.direction[0] == 1:
                self.direction[0] = 0
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            if self.direction[1] == 1:
                self.direction[1] = 0

        # Move
        if not self.down:
            self.pos[0] += self.direction[0] * self.move_speed * self.runner.tick
            self.pos[1] += self.direction[1] * self.move_speed * self.runner.tick
            self.color = self.normal_color
        if self.down:
            self.color = self.down_color
            if self.watching_player.down:
                self.down = False
        
        # Update rect position for drawing
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


        # Set look direction if moving
        if not self.direction == [0, 0]:
            # If direction changed
            if self.direction != self.look_direction:
                # Update the texture
                self.update_texture()
                pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0, 0, self.width, self.height), 2)
                

            self.look_direction = self.direction

        # For trails
        self.image = self.surface




        
    def do_rotate(self, dir):
        left = -90
        right = 90
        surface = self.surface
        if dir == [0, 1]:
            surface = pygame.transform.rotate(self.surface, left)
        if dir == [0, -1]:
            surface = pygame.transform.rotate(self.surface, right)
        if dir == [-1, 0]:
            surface = pygame.transform.rotate(self.surface, right * 2)
        if dir == [1, 0]:
            pass # Already looking this way
        return surface

        

    def draw(self, screen):

        head_radius = self.width * 0.5

        upways = False
        if not self.look_direction[1] == 0:
            upways = True
        
        funky_look_direction = [self.look_direction[0], self.look_direction[1]]
        
        if upways:
            funky_look_direction[0] = 0


        # the offset for the weird thing
        offset = 0.1

        # draw the thing
        if upways:
            thing_pos = [(self.rect.centerx - head_radius * 5 / 2 + self.width * offset * self.look_direction[0]), 
                        (self.rect.centery - head_radius * 3.5 / 2 + self.height * offset * self.look_direction[1])]
        else:
            thing_pos = [(self.rect.centerx - head_radius * 3.5 / 2 + self.width * offset * funky_look_direction[0]), 
                        (self.rect.centery - head_radius * 5 / 2 + self.height * offset * self.look_direction[1])]
        funky_graphics.draw_player(head_radius, self.color, thing_pos, screen, funky_look_direction)

        # Draw the player
        if False: #dont draw player
            screen.blit(self.surface, self.rect)

       

        # Draw the ball on player if the player has the ball
        if self.has_ball:
            self.ball.rect.center = self.rect.center
            screen.blit(self.ball.image, self.ball.rect)




    def throw(self, speed):
        
        if self.has_ball and not self.down:
            lx = self.look_direction[0]
            ly = self.look_direction[1]
            self.ball.rect.center = self.rect.center
            self.ball.rect.x += lx * self.width + lx * self.ball.radius
            self.ball.rect.y += ly * self.height + ly * self.ball.radius
            self.ball.v = np.array(self.look_direction, dtype='float64') * speed
            self.ball.flying = True
            self.ball.flying_timer = self.ball.max_flying_timer * speed
            self.ball.player = self
            self.runner.balls.add(self.ball)
        self.has_ball = False
        self.ball = None

    def debug_line(self, screen, debug_v):
        # Debug for drawing direction of look_direction
        pygame.draw.aaline(screen, (self.color), self.pos,  [self.pos[0] + debug_v[0] * self.width * 2, self.pos[1] + debug_v[1] * self.width * 2])

    def update_controls(self, index, status):
        if not status == None:
            self.control_status[index] = status