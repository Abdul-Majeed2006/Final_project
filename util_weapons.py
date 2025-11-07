import pygame
from util_params import *
import math
from util_sight import *
from util_bullet import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.weapons = [{'rifle':'assets/weapons/tile_0005.png',
                         'aim':'assets/weapons/tile_0039.png',
                         'round':30,'damage':5}]
        self.current_weapon = self.weapons[0]
        # ammo
        self.ammo =self.current_weapon['round']
        self.max_ammo = 30
        #load rifle image
        rifle = self.current_weapon['rifle']
        self.image = pygame.image.load(rifle)
        self.image = pygame.transform.rotozoom(self.image,0,2)
        self.rect = self.image.get_rect()
        # position of gun is gonna be position of player
        self.rect = self.image.get_rect()
        self.rect.center = self.player.rect.center
        # sight
        aim = self.current_weapon['aim']
        self.sight = Sight(aim)
        #create bullet group for the rifle
        self.bullet_group = pygame.sprite.Group()
       
    def update(self):
        # well use cursor to aim 
        #get cursor x and y
        mouse_pos = pygame.mouse.get_pos()
        #lets calculate the vector from player to mouse
        delta_x = mouse_pos[0] - self.player.rect.centerx
        delta_y = mouse_pos[1] - self.player.rect.centery
        #calculate the angle, convert to degrees, pygame accept degrees only
        self.angle = math.atan2(delta_y,delta_x)
        angle_degrees = math.degrees(self.angle)
        #well roate the gun with the cursor so it points at what its aiming
        self.image = pygame.transform.rotozoom(self.image,-self.angle,1)
        #the weapons position shoiuld  be thesame with the players position
        self.rect = self.image.get_rect(center = self.player.rect.center)
        #update sight
        self.sight.update()
        #update bullet
        self.bullet_group.update()

    def shoot(self):
        #player calls funnction by clicking on mouse
        if self.ammo > 0 :
            self.ammo -= 1
            print(f'{self.ammo}/{self.max_ammo}')
            new_bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
            self.bullet_group.add(new_bullet)
        else:
            print('reload')
        

    def reload(self):
        #player calls function by clicking on a key
        print('reloading')
        self.ammo = self.max_ammo

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        #draw the sight
        self.sight.draw(screen)
        # draw the bullet
        self.bullet_group.draw(screen)