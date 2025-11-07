import pygame
from util_params import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,enemy):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.enemy = enemy
        self.weapons = [{'rifle':'assets/weapons/tile_0005.png','aim':'assets/weapons/tile_0034.png','round':30,'damage':5}]
                        #{'sniper':'assets/weapons/tile_0003.png','aim':'assets/weapons/tile_0035.png','round':5,'damage':15}
        #lets figure out one weapon first
        self.current_weapon = self.weapons[0]
        #load rifle image
        rifle = self.current_weapon['rifle']
        self.image = pygame.image.load(rifle)
        self.rect = self.image.get_rect()
        # position of gun is gonna be position of player
        self.rect.center = self.player.rect.center
       

    def update(self):
        # update position of wepon to always be with the player
        self.rect.center = self.player.rect.center



    def draw(self,screen):
        screen.blit(self.image, self.rect)