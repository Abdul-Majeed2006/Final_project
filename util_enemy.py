import pygame
from util_params import *
from random import choice, randint
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.live = 1
        self.x = x
        self.y = y
        # enemy health
        self.health = 10
        self.enemy = ['assets/players/tile_0013.png',
                 'assets/players/tile_0010.png',
                 ]
        self.fp = choice(self.enemy)
        self.image = pygame.image.load(self.fp)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        # explode and does damage to the player
        self.damage = 10

        #speed
        self.vx = randint(-2,2)
        self.vy = randint(-2,2)
        self.speed = randint(1,2)
        # angle to player 
        self.theta = 0 

    def get_theta(self):
        delta_x = self.player.rect.centerx - self.x
        delta_y = self.player.rect.centery - self.y
        # a tan2 because tan is negative in some quadrants, tHis makes it always positive
        self.theta = math.atan2(delta_y, delta_x)


    def update(self):
        #update theta
        self.get_theta()
        # update speed of fish
        self.vx = self.speed * math.cos(self.theta)
        self.vy = self.speed * math.sin(self.theta)
        # update positioon
        self.x += self.vx
        self.y += self.vy
        #update rect
        self.rect.center = (self.x,self.y)
        # if enemy rect = player rect en

    def take_damage(self,amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
        
    def draw(self,screen):
        screen.blit(self.image, self.rect)