import pygame
import os
from .util_params import *
from random import choice

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health = 30
        
        # Randomly choose between Crate and Barrel
        # assets/bg/tile_0036.png (Crate), tile_0038.png (Metal Barrel)
        types = [
            {'image': 'tile_0036.png', 'hp': 20},
            {'image': 'tile_0038.png', 'hp': 40}
        ]
        obj_type = choice(types)
        self.health = obj_type['hp']
        
        try:
            path = os.path.join(BG_DIR, obj_type['image'])
            self.image = pygame.image.load(path)
            self.image = pygame.transform.rotozoom(self.image, 0, 2)
        except:
            self.image = pygame.Surface((32, 32))
            self.image.fill((100, 60, 20)) # Brown fallback
            
        self.rect = self.image.get_rect(center=(x, y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True # Destroyed
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
