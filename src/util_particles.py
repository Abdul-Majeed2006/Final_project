import pygame
from random import randint, choice
import math
from .util_params import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, lifetime):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.speed = speed
        self.lifetime = lifetime
        self.original_lifetime = lifetime
        self.x = x
        self.y = y
        
        # Random visual properties
        self.size = randint(4, 8)
        self.angle = randint(0, 360)
        self.angle_rad = math.radians(self.angle)
        self.vx = math.cos(self.angle_rad) * self.speed
        self.vy = math.sin(self.angle_rad) * self.speed
        
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        
        # Shrink over time
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        else:
            # Fade/Shrink Effect
            percent_life = self.lifetime / self.original_lifetime
            current_size = int(self.size * percent_life)
            if current_size > 0:
                 self.image = pygame.transform.scale(self.image, (current_size, current_size))
                 self.rect = self.image.get_rect(center=(self.x, self.y))

class ParticleSystem:
    def __init__(self):
        self.group = pygame.sprite.Group()
        
    def create_explosion(self, x, y, color):
        for _ in range(15): # 15 particles per boom
            speed = randint(2, 6)
            lifetime = randint(20, 40)
            p = Particle(x, y, color, speed, lifetime)
            self.group.add(p)

    def create_muzzle_flash(self, x, y):
         for _ in range(5):
             speed = randint(3, 8)
             lifetime = randint(5, 10)
             p = Particle(x, y, YELLOW, speed, lifetime)
             self.group.add(p)
             
    def create_dash_trail(self, x, y):
        # Static particle that fades quickly
        p = Particle(x, y, LIGHT_GREY, 0, 15)
        p.size = 15 # Start bigger
        self.group.add(p)

    def update(self):
        self.group.update()
        
    def draw(self, screen):
        self.group.draw(screen)
