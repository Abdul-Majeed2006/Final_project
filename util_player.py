import pygame
from util_params import *
from util_weapons import *

class Player(pygame.sprite.Sprite):
    def __init__(self,x = HEIGHT/2, y= WIDTH/2):
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
        #alive to return true 
        self.alive = True
        #make my player tile and get player rect and  player image after death
        self.image = pygame.image.load('assets/players/tile_0006.png')
        self.grave_stone = pygame.image.load('assets/players/gravestone-roof.png')
        # make a left and a right facing image adjuat size of grave stone
        image_right = pygame.transform.rotozoom(self.image,0,2)
        self.image_right = image_right
        self.image_left = pygame.transform.flip(image_right,1,0)
        self.grave_stone = pygame.transform.rotozoom(self.grave_stone,0,2)
        #the first drawn image is looh_righ
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        # create weapon inside player, weapon part of player
        self.weapon = Weapon(self)

    def update(self):
        # update player position
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)
        # update player to look  at left when moving left
        # moving  right
        if self.vx > 0:
            self.image = self.image_right
        # moving left
        if self.vx < 0:
            self.image = self.image_left
        #player should not leave screen
        # max height the player can reach on the screen so he doesnt go out of screen
        height = HEIGHT
        width = WIDTH 
        if self.x < 0:
            self.x = 0
        if self.x > width:
            self.x = width
        if self.y < 0:
            self.y = 0
        # height - height of image
        if self.y > height:
            self.y = height
        
        # call weapon update to update with player
        self.weapon.update()

    # we would make our player using arrows, N//B: clicking a key is an event
    def check_event(self,event):
        if event.type == pygame.KEYDOWN:
        # if a key is being clicked down
            # up arrow move up
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.vy += -2 
            #down arrow move down
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.vy += 2 
            #left arrow move left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                self.vx += -2 
            # right arrow move right
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.vx += 2 
            # we need to reload
            if event.key == pygame.K_r:
                self.reload()
        # stop speed when key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.vy = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.vx =0

        #check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #left mouse click
            self.shoot()

    def shoot(self):
        self.weapon.shoot()
   
    def reload(self):
        self.weapon.reload()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
    
    def die(self):
        self.image = self.grave_stone
        self.vx = 0
        self.vy = 0
        
    def reset(self):
        self.health = self.max_health
        self.image = self.image
        self.x = self.x_o
        self.y = self.y_o
        self.rect = self.image.get_rect(self.x,self.y)
        self.vx = 0
        self.vy = 0
        self.weapon.reload()

    def draw(self,screen):
        #draw player then image
        screen.blit(self.image, self.rect)
        self.weapon.draw(screen)