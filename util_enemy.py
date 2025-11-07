import pygame
from util_params import *

class Ememy(pygame.sprite.Sprite):
    def __init__(self, live ,x ,y ,damage):
        pygame.sprite.Sprite.__init__(self)
        self.live = live
        self.x = x
        self.y = y
        self.damage = damage
        enemy = ['assets/players/tile_0013.png',
                 'assets/players/tile_0010.png',
                 ]