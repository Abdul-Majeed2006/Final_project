import pygame
import os

from .util_params import *
from random import choice, randint
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, wave_number, enemy_type='standard'):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.player = player
        self.wave_number = wave_number
        self.enemy_type = enemy_type
        
        # Base Stats
        base_speed = ENEMY_BASE_SPEED
        self.health = 10
        self.damage = 10
        image_name = 'tile_0013.png' # Default
        
        # Type Specific Stats
        if self.enemy_type == 'scout':
            base_speed = ENEMY_BASE_SPEED * 1.5
            self.health = 5
            image_name = 'tile_0009.png' # Use a distinct sprite
        elif self.enemy_type == 'tank':
            base_speed = ENEMY_BASE_SPEED * 0.5
            self.health = 30
            image_name = 'tile_0008.png'
            self.image = pygame.transform.scale(self.image, (48, 48)) # Make tank bigger? complex with sprite load
            # Lets just keep size same for now to avoid hitbox issues or handle scale below

        # Speed Calculation
        wave_bonus = (wave_number-1) * WAVE_BONUS_SPEED
        random_bonus = randint(0,3) * 0.1
        self.speed = base_speed + wave_bonus + random_bonus
        
        # Load Image
        try:
             self.image = pygame.image.load(os.path.join(PLAYERS_DIR, image_name))
        except:
             self.image = pygame.Surface((32,32))
             self.image.fill(RED)

        # Scale Tank if needed (after load)
        if self.enemy_type == 'tank':
             self.image = pygame.transform.scale(self.image, (40, 40)) # Slightly larger

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Floating point position for smooth movement
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def update(self):
        # Calculate direction to player
        delta_x = self.player.rect.centerx - self.rect.centerx
        delta_y = self.player.rect.centery - self.rect.centery
        angle = math.atan2(delta_y, delta_x)
        
        # Move
        self.pos_x += math.cos(angle) * self.speed
        self.pos_y += math.sin(angle) * self.speed
        
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def get_safe_spawn_position(player_rect, buffer_distance=200):
    """
    Generates a random (x, y) coordinate that is at least `buffer_distance` pixels 
    away from the player.
    """
    while True:
        x_pos = randint(0, WIDTH)
        y_pos = randint(0, HEIGHT)
        
        # Calculate distance to player
        dx = x_pos - player_rect.centerx
        dy = y_pos - player_rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance >= buffer_distance:
            return x_pos, y_pos