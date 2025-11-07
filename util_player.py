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
        self.image = pygame.image.load('assets/players/tile_0006.png')
        self.rect = self.image.get_rect()
        
        
        


        # increase player size
        self.image = pygame.transform.rotozoom(self.image,0,2)



    
    def update(self):
        # update player position
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)
        #player should not leave screen
        # max height the player can reach on the screen so he doesnt go out of screen
        h = self.image.get_height()
        height = HEIGHT- h
        w = self.image.get_width()
        width = WIDTH - w
        if self.x < 0:
            self.x = 0
        if self.x > width:
            self.x = width
        if self.y < 0:
            self.y = 0
        # height - height of image
        if self.y > height:
            self.y = height

        
        

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
       





    def shoot(self):
        # when a key is pressed
        
        shells -= 1

       
    def reload(self):
        #if a key is clicked reload

        shells = 30
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        # update the scores
        score = 0
        score_string = f'{score}'
        #get font
        font = pygame.font.SysFont('Arial',48)
        score_ = font.render(score_string, True,(255,0,0))
        screen.blit(score_,(0,0))