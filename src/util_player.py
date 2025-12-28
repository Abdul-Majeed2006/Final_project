import pygame
import os

from .util_params import *
from .util_weapons import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x=WIDTH/2, y=HEIGHT/2):

        pygame.sprite.Sprite.__init__(self)
        self.x_o = x
        self.x = x
        self.y_o = y
        self.y = y
        self.vx = 0
        self.vy = 0    
        # health
        self.max_health = 100
        self.health = 100
        # alive status
        self.alive = True
        
        # Load images
        try:
            self.image_original = pygame.image.load(os.path.join(PLAYERS_DIR, 'tile_0006.png'))
            self.grave_stone = pygame.image.load(os.path.join(PLAYERS_DIR, 'gravestone-roof.png'))
        except Exception as e:
             # ... (keep fallback)
            print(f"Warning: Could not load player images: {e}")
            self.image_original = pygame.Surface((32, 32))
            self.image_original.fill(WHITE)
            self.grave_stone = pygame.Surface((32, 32))
            self.grave_stone.fill((100, 100, 100))

        # Transformations
        self.image_right = pygame.transform.rotozoom(self.image_original, 0, 2)
        self.image_left = pygame.transform.flip(self.image_right, 1, 0)
        self.grave_stone = pygame.transform.rotozoom(self.grave_stone, 0, 2)
        
        # Initial State
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Weapon
        self.weapon = Weapon(self)
        
        # Dash Mechanics
        self.dash_speed = 15
        self.dash_cooldown = 0
        self.dash_duration = 0
        self.is_dashing = False
        self.dash_vector = (0, 0)

    def update(self, particle_system=None):
        # Handle Cooldowns
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
        # Handle Movement Input
        keys = pygame.key.get_pressed()
        
        # If dashing, force movement
        if self.is_dashing:
            self.vx, self.vy = self.dash_vector
            self.dash_duration -= 1
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.vx = 0
                self.vy = 0
            
            # Create Trail
            if particle_system and self.alive:
                 particle_system.create_dash_trail(self.x, self.y)
        else:
            # Normal Movement
            self.vx = 0
            self.vy = 0
            
            if self.health > 0: # Only move if alive
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.vx = -PLAYER_SPEED
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.vx = PLAYER_SPEED
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.vy = -PLAYER_SPEED
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.vy = PLAYER_SPEED

        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Orientation
        if self.vx > 0:
            self.image = self.image_right
        elif self.vx < 0:
            self.image = self.image_left
            
        # Screen Boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH
            
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT
            
        # Update rect
        self.rect.center = (self.x, self.y)
        
        # Update weapon
        self.weapon.update()

    def check_event(self, event, audio_manager):
        # Only handle discrete actions here (shooting, reloading)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left Click
                self.shoot(audio_manager)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reload()
            if event.key == pygame.K_SPACE:
                self.dash()

    def dash(self):
        if self.dash_cooldown <= 0 and not self.is_dashing and (self.vx != 0 or self.vy != 0):
            self.is_dashing = True
            self.dash_duration = 10 # frames
            self.dash_cooldown = 120 # 2 seconds
            
            # Normalize vector to dash speed
            import math
            mag = math.sqrt(self.vx**2 + self.vy**2)
            if mag > 0:
                self.dash_vector = ((self.vx / mag) * self.dash_speed, (self.vy / mag) * self.dash_speed)


    def shoot(self, audio_manager):
        if self.health > 0:
            self.weapon.shoot(audio_manager)
   
    def reload(self):
        self.weapon.reload()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.die()
    
    def die(self):
        self.image = self.grave_stone
        self.vx = 0
        self.vy = 0
        
    def reset(self):
        self.health = self.max_health
        self.image = self.image_right
        self.x = self.x_o
        self.y = self.y_o
        self.vx = 0
        self.vy = 0
        self.rect.center = (self.x, self.y)
        self.weapon.reload()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.health > 0:
            self.weapon.draw(screen)
