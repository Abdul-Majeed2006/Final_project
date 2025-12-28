import pygame
import os
import math
from .util_params import *
from .util_sight import *
from .util_bullet import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        
        # Weapon Types Configuration
        self.types = {
            'rifle': {
                'image': os.path.join(WEAPONS_DIR, 'tile_0000.png'),
                'aim': os.path.join(WEAPONS_DIR, 'tile_0039.png'), # Precise Dot
                'damage': 5,
                'cooldown': 10, 
                'spread': 1,
                'pellets': 1,
                'sound': 'shoot_rifle',
                'ammo': 30,
                'max_ammo': 30
            },
            'shotgun': {
                'image': os.path.join(WEAPONS_DIR, 'tile_0004.png'), 
                'aim': os.path.join(WEAPONS_DIR, 'tile_0029.png'), # Wide Crosshair (previously mistaken for gun)
                'damage': 4, 
                'cooldown': 45, 
                'spread': 15, 
                'pellets': 5,
                'sound': 'shoot_shotgun',
                'ammo': 12,
                'max_ammo': 12
            },
            'mg': {
                'image': os.path.join(WEAPONS_DIR, 'tile_0003.png'), 
                'aim': os.path.join(WEAPONS_DIR, 'tile_0021.png'), # Tech Crosshair
                'damage': 3, 
                'cooldown': 4, 
                'spread': 5, 
                'pellets': 1,
                'sound': 'shoot_mg',
                'ammo': 100,
                'max_ammo': 100
            }
        }
        
        # Current State
        self.current_type = 'rifle'
        self.load_weapon_stats('rifle')
        
        # Graphics
        self.original_image = pygame.image.load(self.stats['image'])
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, 3)
        self.original_image_flipped = pygame.transform.flip(self.original_image, 0, 1)
        self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect()
        self.rect.center = self.player.rect.center
        
        self.sight = Sight(self.stats['aim'])
        self.bullet_group = pygame.sprite.Group()
        self.angle = 0
        
        # Reload / Firing State
        self.last_shot_time = 0
        self.fire_cooldown_timer = 0
        self.reload_timer = 0
        self.reload_duration = 120 # 2 seconds

    def load_weapon_stats(self, type_name):
        self.current_type = type_name
        self.stats = self.types[type_name]
        self.ammo = self.stats['ammo']
        self.max_ammo = self.stats['max_ammo']
        
        # Reload graphics if needed
        # (Simplified: assumes all guns use similar sprite size/logic, update image in update loop)
        try:
             img = pygame.image.load(self.stats['image'])
             self.original_image = pygame.transform.rotozoom(img, 0, 3)
             self.original_image_flipped = pygame.transform.flip(self.original_image, 0, 1)
        except:
             pass 

    def update(self):
        # Update Position
        self.rect.center = self.player.rect.center
        
        # Cooldowns
        if self.fire_cooldown_timer > 0:
            self.fire_cooldown_timer -= 1
        if self.reload_timer > 0:
            self.reload_timer -= 1
            if self.reload_timer == 0:
                self.ammo = self.max_ammo
        
        # Aiming
        mouse_pos = pygame.mouse.get_pos()
        delta_x = mouse_pos[0] - self.player.rect.centerx
        delta_y = mouse_pos[1] - self.player.rect.centery
        self.angle = math.atan2(delta_y, delta_x)
        angle_degrees = math.degrees(self.angle)
        
        # Flip/Rotate
        if abs(angle_degrees) > 90:
            image = self.original_image_flipped
        else:
            image = self.original_image
        self.image = pygame.transform.rotozoom(image, -angle_degrees, 1)
        self.rect = self.image.get_rect(center=self.player.rect.center)
        
        self.sight.update()
        self.bullet_group.update()

    def shoot(self, audio_manager):
        # Check constraints
        if self.reload_timer > 0:
            return
        if self.fire_cooldown_timer > 0:
            return
            
        if self.ammo > 0:
            self.ammo -= 1
            self.fire_cooldown_timer = self.stats['cooldown']
            
            # Fire logic
            from random import uniform
            
            damage = self.stats['damage']
            spread = self.stats['spread']
            count = self.stats['pellets']
            
            for _ in range(count):
                # Calculate spread angle
                spread_angle = uniform(-spread, spread)
                bullet_angle = self.angle + math.radians(spread_angle)
                
                new_bullet = Bullet(self.rect.centerx, self.rect.centery, bullet_angle, damage)
                self.bullet_group.add(new_bullet)
            
            # Sound
            audio_manager.play(self.stats['sound'])
            
        else:
            # Auto Reload if empty and trying to shoot
            self.reload()

    def reload(self):
        if self.reload_timer == 0 and self.ammo < self.max_ammo:
            self.reload_timer = self.reload_duration
            # print("Reloading...")

    def switch_weapon(self, type_name):
        if type_name in self.types:
            self.load_weapon_stats(type_name)

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        self.sight.draw(screen)
        self.bullet_group.draw(screen)
        
        # Draw Reload Bar if reloading
        if self.reload_timer > 0:
             # Just a small bar above player
             pct = 1 - (self.reload_timer / self.reload_duration)
             pygame.draw.rect(screen, BLACK, (self.rect.centerx - 20, self.rect.top - 15, 40, 5))
             pygame.draw.rect(screen, YELLOW, (self.rect.centerx - 20, self.rect.top - 15, 40 * pct, 5))
