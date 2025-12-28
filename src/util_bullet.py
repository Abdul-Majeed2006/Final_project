import pygame
import math
import os
from .util_params import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle_rads, damage=5):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(os.path.join(WEAPONS_DIR, 'tile_0023.png'))
        except:
            self.image = pygame.Surface((4, 4))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        #save the damage
        self.damage = damage
        # set speed of buller
        speed = 15
        # get vx and vy from angle of weapon to aim
        self.vx = speed * math.cos(angle_rads)
        self.vy = speed * math.sin(angle_rads)

    def update(self):
        # update bullet position bullet
        self.x += self.vx
        self.y += self.vy
        # get position of bullet
        self.rect.center = (self.x, self.y)
        # Kill the bullet if it goes off-screen
        if not (0 < self.rect.centerx < WIDTH and 0 < self.rect.centery < HEIGHT) :
            self.kill() 
        


