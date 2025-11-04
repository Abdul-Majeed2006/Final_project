import pygame
from util_params import *

class Player(pygame.sprite.Sprite):
    def __init__(self,x = HEIGHT/2, y= WIDTH/2 , shells = 30):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.shells = shells
        
        #make my player tile and get player rect
        self.image = pygame.image.load('assets/players/tile_0005.png')
        self.rect = self.image.get_rect()

        # increase player size
        self.image = pygame.transform.rotozoom(self.image,0,5)


    
    def update(self):
        # update player position
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)
        

    # we would make our player using arrows, N//B: clicking a key is an event
    def check_event(self,event):
        if event.type == pygame.KEYDOWN:
        # if a key is being clicked down
            # up arrow move up
            if event.key == pygame.K_UP:
                self.vy += -2 
            #down arrow move down
            if event.key == pygame.K_DOWN:
                self.vy += 2 
            #left arrow move left
            if event.key == pygame.K_LEFT:
                self.vx += -2 
            # right arrow move right
            if event.key == pygame.K_RIGHT:
                self.vx += 2 
       





    def shoot(self):
        # when a key is pressed
        
        shells -= 1

       
    def reload(self):
        #if a key is clicked reload

        shells = 30
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)