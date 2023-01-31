import numpy as np
import pygame

    
def elastic_collision(ball1, ball2):
    v1 = np.array(ball1.v)
    m1 = np.array(ball1.mass)
    v2 = np.array(ball2.v)
    m2 = np.array(ball2.mass)
    x1 = np.array(ball1.rect.center)
    x2 = np.array(ball2.rect.center)

    damping = 0.99

    u1 = ((m1-m2)/(m1+m2)) * v1 + ((2 * m2)/(m1+m2)) * v2
    u2 = ((2 * m1)/(m1+m2)) * v1 + ((m2-m1)/(m1+m2)) * v2


    nv = pygame.Vector2(ball2.rect.center) - pygame.Vector2(ball1.rect.center)

    


    u1 = v1 - ((2 * m2)/(m1+m2)) * (np.dot(v1 - v2, x1 - x2)/np.dot(x1 - x2, x1 - x2)) * (x1 - x2)
    u2 = v2 - ((2 * m1)/(m1+m2)) * (np.dot(v2 - v1, x2 - x1)/np.dot(x2 - x1, x2 - x1)) * (x2 - x1)

    r1 = ball1.radius
    r2 = ball2.radius

    dist = r1 + r2 - np.linalg.norm(x1 - x2)
    direction = (x1 - x2)/np.linalg.norm(x1 - x2)
    v1_in_dir = np.dot(v1, direction)
    v2_in_dir = np.dot(v2, direction)

    ball1.rect.center = x1 + direction * dist * abs(v1_in_dir)/(abs(v1_in_dir) + abs(v2_in_dir))
    ball2.rect.center = x2 - direction * dist * abs(v2_in_dir)/(abs(v1_in_dir) + abs(v2_in_dir))




    newV1 = u1 * damping
    newV2 = u2 * damping
    ball1.v = np.array([newV1[0], newV1[1]], dtype='float64')
    ball2.v = np.array([newV2[0], newV2[1]], dtype='float64')