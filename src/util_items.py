import pygame
from .util_params import *
import os

class HealthPack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = 20
        self.heal_amount = 20
        
        # Procedurally draw a health icon (White square with Red Cross)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, RED, (7, 2, 6, 16)) # Vertical bar
        pygame.draw.rect(self.image, RED, (2, 7, 16, 6)) # Horizontal bar
        
        self.rect = self.image.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 10000 # 10 seconds

    def update(self):
        # Despawn after lifetime
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()
        
        # Simple bobbing animation
        t = pygame.time.get_ticks()
        if (t // 500) % 2 == 0:
            self.rect.centery = self.y - 2
        else:
            self.rect.centery = self.y + 2

class WeaponPickup(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.type = weapon_type
        self.size = 20
        
        # Graphics based on type
        self.image = pygame.Surface((self.size, self.size))
        if weapon_type == 'shotgun':
             self.image.fill((139, 69, 19)) # Brown
        elif weapon_type == 'mg':
             self.image.fill((192, 192, 192)) # Silver
        else:
             self.image.fill(WHITE)
             
        # "W" label
        font = pygame.font.SysFont('Arial', 12, bold=True)
        label = font.render(weapon_type[0].upper(), True, BLACK)
        self.image.blit(label, (5, 5))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 15000 # 15 seconds

    def update(self):
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()

