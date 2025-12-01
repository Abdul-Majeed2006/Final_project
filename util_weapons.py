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
        # save clean copy of image so it doesnt keep blurring out
        original_image = pygame.image.load(rifle)
        # have a normal and a flipped version of image
        self.original_image = pygame.transform.rotozoom(original_image,0,2)
        #flipped
        self.original_image_flipped = pygame.transform.flip(self.original_image,0,1)
        #n//b the imgae thats is gonna be drawn is self.image
        self.image = self.original_image.copy()
        # position of gun is gonna be position of player
        self.rect = self.image.get_rect()
        self.rect.center = self.player.rect.center
        # sight
        aim = self.current_weapon['aim']
        self.sight = Sight(aim)
        #create bullet group for the rifle
        self.bullet_group = pygame.sprite.Group()
        #angle of rotation
        self.angle = 0
        # message to reload
        self.reload_font = pygame.font.SysFont('Arial',30)
        self.reload_timer = 0
        self.reload_message_duration = 300 # 5 secs
        self.reload_message_surface = None 
        # load shoot sound
        self.shoot_sound = pygame.mixer.Sound('assets/Audio/impactMetal_heavy_000.ogg')

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
        # flip gun wto the right or left
        if abs(angle_degrees) > 90:
            image = self.original_image_flipped
        else:
            image = self.original_image
        # rotate the image
        self.image = pygame.transform.rotozoom(image, -angle_degrees,1)

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
            #get damage from the bullet class
            damage = self.current_weapon['damage']
            new_bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle,damage)
            self.bullet_group.add(new_bullet)
            # play shoot sound
            self.shoot_sound.play()
        else:
            print('reload')
            self.reload_timer = self.reload_message_duration
            if not self.reload_message_surface:
                self.reload_message_surface = self.reload_font.render('Reload',True,(255,0,0))
        

    def reload(self):
        #player calls function by clicking on a key
        self.ammo = self.max_ammo
        self.reload_timer = 0

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        #draw the sight
        self.sight.draw(screen)
        # draw the bullet
        self.bullet_group.draw(screen)
        # draw reload
        if self.reload_timer > 0 and self.reload_message_surface:
            message_rect = self.reload_message_surface.get_rect(
                center=(self.player.rect.centerx,(self.player.rect.centery-50)))
            screen.blit(self.reload_message_surface,message_rect)